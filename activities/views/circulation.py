from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin

from activities.models.circulation import (
    EnginImmobilise,
    PieceRetire,
    VitreTeintee,
)
from activities.serializers.circulation import (
    EnginImmobiliseSerializer,
    PieceRetireSerializer,
    VitreTeinteeSerializer,
)

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class EnginImmobiliseViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = EnginImmobiliseSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_immobilisation"]
    ordering_fields = ["date_immobilisation", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "engins_immobilises"

    def get_queryset(self):
        user = self.request.user
        qs = EnginImmobilise.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class PieceRetireViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = PieceRetireSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_retrait"]
    ordering_fields = ["date_retrait", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "pieces_retirées"

    def get_queryset(self):
        user = self.request.user
        qs = PieceRetire.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class VitreTeinteeViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = VitreTeinteeSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_mise"]
    ordering_fields = ["date_mise", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "vitres_teintées"

    def get_queryset(self):
        user = self.request.user
        qs = VitreTeintee.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

# activities/views/circulation.py

from activities.models.circulation import ControleRoutier
from activities.serializers.circulation import ControleRoutierSerializer

class ControleRoutierViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = ControleRoutierSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_controle", "motif"]
    ordering_fields = ["date_controle", "unite", "motif"]
    pagination_class = StandardResultsSetPagination
    basename = "controles_routiers"

    def get_queryset(self):
        user = self.request.user
        qs = ControleRoutier.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)
