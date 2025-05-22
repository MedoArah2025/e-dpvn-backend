from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin
from activities.models.judiciaire import (
    PersonnesInterpelle,
    Gav,
    Deferement,
    Plainte,
    DeclarationVol,
    Infraction,
    SaisieDrogue,
    AutreSaisie,
    Requisition,
    Incendie,
    Noyade,
    DecouverteCadavre,
    PersonnesEnleve,
    VehiculeEnleve,
)
from activities.serializers.judiciaire import (
    PersonnesInterpelleSerializer,
    GavSerializer,
    DeferementSerializer,
    PlainteSerializer,
    DeclarationVolSerializer,
    InfractionSerializer,
    SaisieDrogueSerializer,
    AutreSaisieSerializer,
    RequisitionSerializer,
    IncendieSerializer,
    NoyadeSerializer,
    DecouverteCadavreSerializer,
    PersonnesEnleveSerializer,
    VehiculeEnleveSerializer,
)

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class BaseJudiciaireViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    """
    Base pour les endpoints judiciaires :
    - permissions (admin full, direction/agent pas delete)
    - filtres unit/date/catégorie
    - pagination
    - GET …/export/ → export Excel
    """
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filterset_fields = ()
    basename = "judiciaire"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class PersonnesInterpelleViewSet(BaseJudiciaireViewSet):
    queryset = PersonnesInterpelle.objects.all()
    serializer_class = PersonnesInterpelleSerializer
    filterset_fields = ("unite", "date_interpellation")
    basename = "interpellations"

class GavViewSet(BaseJudiciaireViewSet):
    queryset = Gav.objects.all()
    serializer_class = GavSerializer
    filterset_fields = ("unite", "date_interpellation")
    basename = "gav"

class DeferementViewSet(BaseJudiciaireViewSet):
    queryset = Deferement.objects.all()
    serializer_class = DeferementSerializer
    filterset_fields = ("unite", "date_interpellation")
    basename = "deferements"

class PlainteViewSet(BaseJudiciaireViewSet):
    queryset = Plainte.objects.all()
    serializer_class = PlainteSerializer
    filterset_fields = ("unite", "date_plainte")
    basename = "plaintes"

class DeclarationVolViewSet(BaseJudiciaireViewSet):
    queryset = DeclarationVol.objects.all()
    serializer_class = DeclarationVolSerializer
    filterset_fields = ("unite", "date_plainte")
    basename = "declaration_vols"

class InfractionViewSet(BaseJudiciaireViewSet):
    queryset = Infraction.objects.all()
    serializer_class = InfractionSerializer
    filterset_fields = ("unite", "categorie_infraction", "date_infraction")
    basename = "infractions"

class SaisieDrogueViewSet(BaseJudiciaireViewSet):
    queryset = SaisieDrogue.objects.all()
    serializer_class = SaisieDrogueSerializer
    filterset_fields = ("unite", "date_saisie")
    basename = "saisies_drogue"

class AutreSaisieViewSet(BaseJudiciaireViewSet):
    queryset = AutreSaisie.objects.all()
    serializer_class = AutreSaisieSerializer
    filterset_fields = ("unite", "date_saisie")
    basename = "autres_saisies"

class RequisitionViewSet(BaseJudiciaireViewSet):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    filterset_fields = ("unite", "date_mise")
    basename = "requisitions"

class IncendieViewSet(BaseJudiciaireViewSet):
    queryset = Incendie.objects.all()
    serializer_class = IncendieSerializer
    filterset_fields = ("unite", "date_signalement")
    basename = "incendies"

class NoyadeViewSet(BaseJudiciaireViewSet):
    queryset = Noyade.objects.all()
    serializer_class = NoyadeSerializer
    filterset_fields = ("unite", "date_noyade")
    basename = "noyades"

class DecouverteCadavreViewSet(BaseJudiciaireViewSet):
    queryset = DecouverteCadavre.objects.all()
    serializer_class = DecouverteCadavreSerializer
    filterset_fields = ("unite", "date_signalement")
    basename = "decouvertes_cadavre"

class PersonnesEnleveViewSet(BaseJudiciaireViewSet):
    queryset = PersonnesEnleve.objects.all()
    serializer_class = PersonnesEnleveSerializer
    filterset_fields = ("unite", "date_mise")
    basename = "personnes_enlevees"

class VehiculeEnleveViewSet(BaseJudiciaireViewSet):
    queryset = VehiculeEnleve.objects.all()
    serializer_class = VehiculeEnleveSerializer
    filterset_fields = ("unite", "date_mise")
    basename = "vehicules_enleves"

# activities/views/judiciaire.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Prefetch, Q
from activities.models.judiciaire import Infraction
from geodata.models import Quartier
from activities.serializers.judiciaire import InfractionSerializer


class InfractionsGroupByQuartier(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtres dynamiques
        period = request.GET.get('period')
        inf_type = request.GET.get('type')
        unite = request.GET.get('unite')

        qs = Infraction.objects.all()

        # ----- GESTION DES DROITS -----
        user = request.user
        if not (user.is_superuser or user.is_staff or user.role in ["admin", "direction"] or
                (hasattr(user, 'roles') and ("admin" in user.roles or "direction" in user.roles))):
            qs = qs.filter(unite=user.unite)
        # ----- FIN GESTION DES DROITS -----

        if period and period != "all":
            from django.utils.timezone import now
            today = now().date()
            if period == "month":
                qs = qs.filter(date_infraction__month=today.month, date_infraction__year=today.year)
            elif period == "year":
                qs = qs.filter(date_infraction__year=today.year)
            elif period == "week":
                qs = qs.filter(date_infraction__week=today.isocalendar()[1], date_infraction__year=today.year)
            elif period == "today":
                qs = qs.filter(date_infraction=today)

        # CORRECTION ICI : utiliser le bon champ du modèle
        if inf_type and inf_type != "all":
            qs = qs.filter(categorie_infraction=inf_type)
        if unite and unite != "all":
            qs = qs.filter(unite_id=unite)

        # Groupement par quartier
        quartiers = Quartier.objects.all().order_by('nom')
        results = []
        for quartier in quartiers:
            infra_qs = qs.filter(quartier__id=quartier.id)
            infs = list(infra_qs.order_by('-date_infraction')[:30])
            results.append({
                "quartier_id": quartier.id,
                "quartier_nom": quartier.nom,
                "nb_infractions": infra_qs.count(),
                "infractions": InfractionSerializer(infs, many=True).data,
            })

        return Response(results)
