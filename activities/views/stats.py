import csv
import io
from collections import defaultdict
from datetime import datetime

from django.http import HttpResponse
from django.db.models import Count, Sum, IntegerField, FloatField, DecimalField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, PermissionDenied

from activities.models.administratif import (
    AutresDeclarations, Procuration, DeclarationPerte,
    Residence, Cin, AmendeForfaitaire
)
from activities.models.circulation import EnginImmobilise, PieceRetire, VitreTeintee, ControleRoutier
from activities.models.constat import AccidentCirculation
from activities.models.dispositions import (
    MiseslctCto, MiseDPJ, MiseDispositionOcrit, MiseDispositionDouane,
    MiseDST, MiseDPMF, MisePavillonE, MiseSoniloga
)
from activities.models.operations import Positionnement, ServiceOrdre, Patrouille, CoupPoing, Raffle, Descente
from activities.models.judiciaire import (
    PersonnesInterpelle, Gav, Deferement, Plainte,
    DeclarationVol, Infraction, SaisieDrogue, AutreSaisie,
    Requisition, Incendie, Noyade, DecouverteCadavre,
    PersonnesEnleve, VehiculeEnleve
)
from activities.models.rh import EffectifRH
from activities.models.spja import MiseADispositionSpja
# -------------------------------------------------------------------
# Fonction sécurisée d'accès par unité/admin/direction
# -------------------------------------------------------------------
def check_access_or_403(user, unit_id):
    # ADMIN/DIRECTION peuvent tout voir
    if (
        getattr(user, "is_superuser", False)
        or getattr(user, "role", None) in ("admin", "direction")
        or "admin" in getattr(user, "roles", [])
        or "direction" in getattr(user, "roles", [])
    ):
        return
    # Pour les autres : accès seulement à LEUR unité
    if str(getattr(user, "unite_id", "")) != str(unit_id):
        raise PermissionDenied("Vous ne pouvez accéder qu'aux stats de votre unité.")


# -------------------------------------------------------------------
# Mapping complet : (Model, json_key, date_field, group_slug)
# -------------------------------------------------------------------
MODEL_MAP = [
    # Administratif
    (AutresDeclarations,  "autres_declarations",    "date_declaration",     "administratif"),
    (Procuration,         "procurations",           "date_etablissement",   "administratif"),
    (DeclarationPerte,    "declarations_perte",     "date_etablissement",   "administratif"),
    (Residence,           "certificats_residence",  "date_etablissement",   "administratif"),
    (Cin,                 "cin",                    "date_etablissement",   "administratif"),
    (AmendeForfaitaire,   "amendes_forfaitaires",   "date",                 "administratif"),

    # Circulation
    (EnginImmobilise,     "engins_immobilises",     "date_immobilisation",  "circulation"),
    (PieceRetire,         "pieces_retirees",        "date_retrait",         "circulation"),
    (VitreTeintee,        "vitres_teintees",        "date_mise",            "circulation"),
    (ControleRoutier,     "controles_routiers",     "date_controle",        "circulation"),
    # Constat
    (AccidentCirculation, "accidents_circulation",  "date",                 "constat"),

    # Dispositions
    (MiseslctCto,         "slct_cto",               "date_mise",            "disposition"),
    (MiseDPJ,             "dpj",                    "date_mise",            "disposition"),
    (MiseDispositionOcrit,"ocr_im",                 "date_mise",            "disposition"),
    (MiseDispositionDouane,"douane",                "date_mise",            "disposition"),
    (MiseDST,             "dst",                    "date_mise",            "disposition"),
    (MiseDPMF,            "dpmf",                   "date_mise",            "disposition"),
    (MisePavillonE,       "pavillon_e",             "date_mise",            "disposition"),
    (MiseSoniloga,        "soniloga",               "date_mise",            "disposition"),

    # Operation
    (Positionnement,      "positionnements",        "date_operation",       "operation"),
    (ServiceOrdre,        "services_ordre",         "date_operation",       "operation"),
    (Patrouille,          "patrouilles",            "date_operation",       "operation"),
    (CoupPoing,           "coups_poing",            "date_operation",       "operation"),
    (Raffle,              "raffles",                "date_operation",       "operation"),
    (Descente,            "descentes",              "date_operation",       "operation"),

    # Judiciaire
    (PersonnesInterpelle, "interpellations",        "date_interpellation",  "judiciaire"),
    (Gav,                 "gav",                    "date_interpellation",  "judiciaire"),
    (Deferement,          "deferements",            "date_interpellation",  "judiciaire"),
    (Plainte,             "plaintes",               "date_plainte",         "judiciaire"),
    (DeclarationVol,      "declaration_vols",       "date_plainte",         "judiciaire"),
    (Infraction,          "infractions",            "date_infraction",      "judiciaire"),
    (SaisieDrogue,        "saisies_drogue",         "date_saisie",          "judiciaire"),
    (AutreSaisie,         "autres_saisies",         "date_saisie",          "judiciaire"),
    (Requisition,         "requisitions",           "date_mise",            "judiciaire"),
    (Incendie,            "incendies",              "date_signalement",     "judiciaire"),
    (Noyade,              "noyades",                "date_noyade",          "judiciaire"),
    (DecouverteCadavre,   "decouvertes_cadavre",    "date_signalement",     "judiciaire"),
    (PersonnesEnleve,     "personnes_enlevees",     "date_mise",            "judiciaire"),
    (VehiculeEnleve,      "vehicules_enleves",      "date_mise",            "judiciaire"),

    # RH
    (EffectifRH,          "effectif_rh",            "date_rapport",         "rh"),



    (MiseADispositionSpja, "mises_a_disposition_spja", "date_mise", "spja"),


]

# -------------------------------------------------------------------
# Fonctions de troncature
# -------------------------------------------------------------------
TRUNC_FUNCS = {
    "daily":     TruncDay,
    "weekly":    TruncWeek,
    "monthly":   TruncMonth,
    "quarterly": TruncQuarter,
    "yearly":    TruncYear,
}

# -------------------------------------------------------------------
# Pagination standard (si jamais)
# -------------------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    max_page_size = 100

# -------------------------------------------------------------------
# 1) STATS PAR UNITÉ (JSON ou CSV)
# -------------------------------------------------------------------
def get_numeric_fields(model):
    """Retourne tous les champs numériques pertinents (hors id/FK) à totaliser."""
    return [
        f.name
        for f in model._meta.get_fields()
        if (
            isinstance(f, (IntegerField, FloatField, DecimalField))
            and not f.auto_created   # ignore les FK automatiques et reverse FK
            and f.name != "id"
            and not getattr(f, "related_model", False)  # ignore FK
        )
    ]

class StatisticsByUnitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, unit_id):
        check_access_or_403(request.user, unit_id)

        start = request.query_params.get("start")
        end   = request.query_params.get("end")
        try:
            if start: start = datetime.fromisoformat(start)
            if end:   end   = datetime.fromisoformat(end)
        except ValueError:
            raise ValidationError("Dates must be ISO format YYYY-MM-DD")

        groups = request.query_params.get("groups")
        wanted = None
        if groups:
            wanted = {g.strip() for g in groups.split(",")}
            all_groups = {g for *_, g in MODEL_MAP}
            invalid = wanted - all_groups
            if invalid:
                raise ValidationError(f"Groupes inconnus : {', '.join(invalid)}")

        stats = {}
        for model, key, date_field, group in MODEL_MAP:
            if wanted and group not in wanted:
                continue
            qs = model.objects.filter(unite_id=unit_id)
            if start: qs = qs.filter(**{f"{date_field}__gte": start})
            if end:   qs = qs.filter(**{f"{date_field}__lte": end})

            count = qs.count()
            # 🔥 Totaux dynamiques sur toutes les colonnes numériques pertinentes (hors id/FK)
            num_fields = get_numeric_fields(model)
            totals = {fld: qs.aggregate(t=Sum(fld))["t"] or 0 for fld in num_fields}

            stats[key] = {"group": group, "count": count, "totals": totals}

        payload = {
            "unit":   unit_id,
            "start":  start.isoformat() if start else None,
            "end":    end.isoformat()   if end   else None,
            "groups": sorted(wanted) if wanted else "all",
            "stats":  stats,
        }

        if request.query_params.get("export") == "csv":
            return self._export_csv(payload)
        return Response(payload)

    def _export_csv(self, data):
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["key", "group", "count", "totals"])
        for key, info in data["stats"].items():
            writer.writerow([key, info["group"], info["count"], info["totals"]])
        resp = HttpResponse(buf.getvalue(), content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="stats_unit.csv"'
        return resp

# -------------------------------------------------------------------
# 2) STATS GLOBALES (JSON)
# -------------------------------------------------------------------
class StatisticsGlobalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (
            getattr(user, "is_superuser", False)
            or getattr(user, "role", None) in ("admin", "direction")
            or "admin" in getattr(user, "roles", [])
            or "direction" in getattr(user, "roles", [])
        ):
            raise PermissionDenied("Accès réservé à l’administration.")

        period = request.query_params.get("period", "monthly")
        fn = TRUNC_FUNCS.get(period)
        if not fn:
            raise ValidationError(
                "period must be one of: " + ", ".join(TRUNC_FUNCS.keys())
            )

        trend = defaultdict(list)
        for model, key, date_field, *_ in MODEL_MAP:
            qs = model.objects.annotate(period=fn(date_field))
            grouped = qs.values("period").annotate(count=Count("pk")).order_by("period")
            trend[key] = [
                {
                    "period": g["period"].isoformat() if hasattr(g["period"], "isoformat") else str(g["period"]),
                    "count": g["count"]
                }
                for g in grouped
            ]

        return Response({"period": period, "trend": trend})

# -------------------------------------------------------------------
# 2) STATS GlobalFlat (JSON)
# -------------------------------------------------------------------
class StatisticsGlobalFlatView(APIView):
    """
    Statistiques globales totales pour chaque activité (toutes unités, tous les enregistrements).
    Accessible uniquement à admin/direction.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Vérification d’accès (admin ou direction uniquement)
        if not (
            getattr(user, "is_superuser", False)
            or getattr(user, "role", None) in ("admin", "direction")
            or "admin" in getattr(user, "roles", [])
            or "direction" in getattr(user, "roles", [])
        ):
            raise PermissionDenied("Accès réservé à l’administration.")

        stats = {}
        for model, key, date_field, group in MODEL_MAP:
            qs = model.objects.all()
            count = qs.count()
            num_fields = get_numeric_fields(model)
            totals = {fld: qs.aggregate(t=Sum(fld))["t"] or 0 for fld in num_fields}
            stats[key] = {"group": group, "count": count, "totals": totals}
        return Response({"stats": stats})
