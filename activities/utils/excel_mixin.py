# activities/utils/excel_mixin.py

from rest_framework.decorators import action
from rest_framework import status
from openpyxl import Workbook
from io import BytesIO
from django.http import HttpResponse

class ExcelExportMixin:
    @action(detail=False, methods=["get"])
    def export(self, request):
        """
        GET /api/<resource>/export/
        """
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        data = serializer.data  # liste de dicts

        if not data:
            return Response({"detail": "No data to export"}, status=status.HTTP_204_NO_CONTENT)

        # En-têtes
        headers = list(data[0].keys())
        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        for item in data:
            ws.append([item.get(h) for h in headers])

        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        resp = HttpResponse(
            stream.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        resp["Content-Disposition"] = f'attachment; filename="{self.basename}_export.xlsx"'
        return resp
