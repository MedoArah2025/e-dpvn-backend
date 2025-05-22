# activities/views/mixins.py

from io import BytesIO
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.response import Response


class ExcelExportMixin:
    """
    Si on passe ?export=xlsx sur un endpoint ListModelMixin,
    génère un fichier .xlsx au lieu du JSON classique.
    """
    # Nom de fichier par défaut, à surcharger dans le ViewSet si besoin
    export_filename = "export.xlsx"

    def list(self, request, *args, **kwargs):
        # on récupère le queryset filtré / paginé
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        data = self.get_serializer(page or qs, many=True).data

        # si on demande l'export Excel
        if request.query_params.get("export") == "xlsx":
            wb = Workbook()
            ws = wb.active

            if not data:
                ws.append(["No data"])
            else:
                # en-têtes (colonnes)
                headers = list(data[0].keys())
                ws.append(headers)

                # chaque ligne
                for item in data:
                    ws.append([item.get(col) for col in headers])

            buf = BytesIO()
            wb.save(buf)
            buf.seek(0)

            resp = HttpResponse(
                buf.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            resp["Content-Disposition"] = (
                f'attachment; filename="{self.export_filename}"'
            )
            return resp

        # sinon, JSON normal
        return super().list(request, *args, **kwargs)
