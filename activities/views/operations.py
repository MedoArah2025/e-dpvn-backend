from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin
from activities.models.operations import (
    Positionnement,
    ServiceOrdre,
    Patrouille,
    CoupPoing,
    Raffle,
    Descente,
)
from activities.serializers.operations import (
    PositionnementSerializer,
    ServiceOrdreSerializer,
    PatrouilleSerializer,
    CoupPoingSerializer,
    RaffleSerializer,
    DescenteSerializer,
)

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class BaseOperationViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    """
    Base pour les opérations :
    - permissions (admin total, direction/agent pas delete)
    - filtres unit/date_operation
    - tri par date_operation ou unite
    - pagination standard
    - GET …/export/ → export Excel
    """
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_operation"]
    ordering_fields = ["date_operation", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "operations"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class PositionnementViewSet(BaseOperationViewSet):
    queryset = Positionnement.objects.all()
    serializer_class = PositionnementSerializer
    basename = "positionnements"

class ServiceOrdreViewSet(BaseOperationViewSet):
    queryset = ServiceOrdre.objects.all()
    serializer_class = ServiceOrdreSerializer
    basename = "services_ordre"

class PatrouilleViewSet(BaseOperationViewSet):
    queryset = Patrouille.objects.all()
    serializer_class = PatrouilleSerializer
    basename = "patrouilles"

class CoupPoingViewSet(BaseOperationViewSet):
    queryset = CoupPoing.objects.all()
    serializer_class = CoupPoingSerializer
    basename = "coups_poing"

class RaffleViewSet(BaseOperationViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    basename = "raffles"

class DescenteViewSet(BaseOperationViewSet):
    queryset = Descente.objects.all()
    serializer_class = DescenteSerializer
    basename = "descentes"
