from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.models.rh import EffectifRH
from activities.serializers.rh import EffectifRHSerializer
from activities.utils.excel_mixin import ExcelExportMixin

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class EffectifRHViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    """
    CRUD des effectifs RH.
    - Filtrable par unité et date_rapport.
    - Tri possible sur date_rapport et unité.
    - Pagination standard (20 items/page).
    - GET /api/rh/effectifs/export/ pour récupérer un .xlsx de tous les effectifs.
    """
    queryset = EffectifRH.objects.all()
    serializer_class = EffectifRHSerializer
    permission_classes = PERMS

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_rapport"]
    ordering_fields = ["date_rapport", "unite"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        # Admin et Direction voient tout, sinon filtré par unité
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)
