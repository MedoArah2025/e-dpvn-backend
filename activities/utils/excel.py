# activities/utils/excel.py

from io import BytesIO
from openpyxl import Workbook
from django.http import HttpResponse

def build_workbook(headers: list[str], rows: list[list]):
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for row in rows:
        ws.append(row)
    return wb

def workbook_to_response(wb, filename: str):
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    resp = HttpResponse(
        stream.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    return resp
