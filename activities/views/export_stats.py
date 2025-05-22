# activities/views/export_stats.py

import csv
from io import StringIO, BytesIO
from collections import OrderedDict
from datetime import datetime

from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

from activities.views.stats import MODEL_MAP  # mapping centralisé
from activities.utils.stats_permissions import can_access_unit_stats, check_access_or_403

class ExportStatsView(APIView):
    """
    GET /api/statistics/units/{unit_id}/export/?start=&end=&groups=
    GET /api/statistics/export/?unit_id=&start=&end=&format=csv|xlsx
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, unit_id=None):
        """
        Exporte les statistiques d'une unité ou globales (admin seulement).
        """
        user = request.user

        # Récupération des paramètres
        unit_id_param = unit_id or request.query_params.get("unit_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        groups = request.query_params.get("groups")
        fmt = request.query_params.get("format", "xlsx").lower()

        # Validation des groupes
        wanted = None
        if groups:
            wanted = {g.strip() for g in groups.split(",")}
            all_groups = {g for *_, g in MODEL_MAP}
            invalid = wanted - all_groups
            if invalid:
                raise ValidationError(f"Groupes inconnus : {', '.join(invalid)}")

        # Cas : export d'une unité précise
        if unit_id_param:
            check_access_or_403(user, unit_id_param)
            rows = []
            header = ["unite", "stat_key", "count"]
            totals_fields = []

            for Model, key, date_field, group in MODEL_MAP:
                if wanted and group not in wanted:
                    continue
                qs = Model.objects.filter(unite_id=unit_id_param)
                if start:
                    qs = qs.filter(**{f"{date_field}__gte": start})
                if end:
                    qs = qs.filter(**{f"{date_field}__lte": end})
                count = qs.count()
                num_fields = [
                    f.name for f in Model._meta.fields
                    if f.get_internal_type() in ("IntegerField", "FloatField", "DecimalField")
                ]
                for fld in num_fields:
                    col = f"total_{fld}"
                    if col not in totals_fields:
                        totals_fields.append(col)
                        header.append(col)
                totals = OrderedDict((f"total_{fld}", qs.aggregate(sum=Sum(fld))["sum"] or 0)
                                     for fld in num_fields)
                row = {
                    "unite":      unit_id_param,
                    "stat_key":   key,
                    "count":      count,
                    **totals
                }
                rows.append(row)

            if fmt == "csv":
                return self._export_csv(header, rows, filename=f"stats_unit_{unit_id_param}.csv")
            else:
                return self._export_xlsx(header, rows, filename=f"stats_unit_{unit_id_param}.xlsx")

        # Cas : export global (multi-unité, réservé à admin/direction/superuser)
        else:
            if not (user.is_superuser or getattr(user, "role", None) in ("admin", "direction")):
                raise PermissionDenied("Export global réservé à l'administration.")

            rows = []
            header = ["unite", "stat_key", "count"]
            totals_fields = []

            for Model, key, date_field, group in MODEL_MAP:
                if wanted and group not in wanted:
                    continue
                qs = Model.objects.all()
                if start:
                    qs = qs.filter(**{f"{date_field}__gte": start})
                if end:
                    qs = qs.filter(**{f"{date_field}__lte": end})
                for unit in qs.values_list("unite_id", flat=True).distinct():
                    qs_unit = qs.filter(unite_id=unit)
                    count = qs_unit.count()
                    num_fields = [
                        f.name for f in Model._meta.fields
                        if f.get_internal_type() in ("IntegerField", "FloatField", "DecimalField")
                    ]
                    for fld in num_fields:
                        col = f"total_{fld}"
                        if col not in totals_fields:
                            totals_fields.append(col)
                            header.append(col)
                    totals = OrderedDict((f"total_{fld}", qs_unit.aggregate(sum=Sum(fld))["sum"] or 0)
                                         for fld in num_fields)
                    row = {
                        "unite":      unit,
                        "stat_key":   key,
                        "count":      count,
                        **totals
                    }
                    rows.append(row)

            if fmt == "csv":
                return self._export_csv(header, rows, filename="stats_global.csv")
            else:
                return self._export_xlsx(header, rows, filename="stats_global.xlsx")

    def _export_csv(self, header, rows, filename):
        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=header)
        writer.writeheader()
        for row in rows:
            for h in header:
                row.setdefault(h, "")
            writer.writerow(row)
        resp = HttpResponse(buf.getvalue(), content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp

    def _export_xlsx(self, header, rows, filename):
        wb = Workbook()
        ws = wb.active
        ws.append(header)
        for row in rows:
            ws.append([row.get(h, "") for h in header])
        buf = BytesIO()
        wb.save(buf)
        resp = HttpResponse(buf.getvalue(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp
