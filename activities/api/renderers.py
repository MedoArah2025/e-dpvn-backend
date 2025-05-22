from rest_framework_xlsx.renderers import XLSXRenderer

class StatisticsXLSXRenderer(XLSXRenderer):
    sheet_name = "Stats"
    header = []        # on remplira dynamiquement en view
    date_format = "YYYY-MM-DD"
