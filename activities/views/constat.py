from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin
from activities.models.constat import AccidentCirculation
from activities.serializers.constat import AccidentCirculationSerializer

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class AccidentCirculationViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    """
    CRUD des constatations d'accidents de circulation.

    - Filtrable par unité et date de l'accident.
    - Tri possible sur la date et l'unité.
    - Pagination standard (20 items par page).
    - GET /api/constats/ → liste
    - GET /api/constats/export/ → export Excel
    """
    serializer_class = AccidentCirculationSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date"]
    ordering_fields = ["date", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "constats"

    def get_queryset(self):
        user = self.request.user
        qs = AccidentCirculation.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)
