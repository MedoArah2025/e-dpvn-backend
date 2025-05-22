from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin

from activities.models.administratif import (
    AutresDeclarations,
    Procuration,
    DeclarationPerte,
    Residence,
    Cin,
    AmendeForfaitaire,
)
from activities.serializers.administratif import (
    AutresDeclarationsSerializer,
    ProcurationSerializer,
    DeclarationPerteSerializer,
    ResidenceSerializer,
    CinSerializer,
    AmendeForfaitaireSerializer,
)

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# --------- LOGIQUE DE FILTRAGE SECURISEE À REPRENDRE PARTOUT ---------

class AutresDeclarationsViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = AutresDeclarationsSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date_declaration')
    pagination_class = StandardResultsSetPagination
    basename = "autres_declarations"

    def get_queryset(self):
        user = self.request.user
        qs = AutresDeclarations.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class ProcurationViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = ProcurationSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date_etablissement')
    pagination_class = StandardResultsSetPagination
    basename = "procurations"

    def get_queryset(self):
        user = self.request.user
        qs = Procuration.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class DeclarationPerteViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = DeclarationPerteSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date_etablissement')
    pagination_class = StandardResultsSetPagination
    basename = "declarations_perte"

    def get_queryset(self):
        user = self.request.user
        qs = DeclarationPerte.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class ResidenceViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = ResidenceSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date_etablissement')
    pagination_class = StandardResultsSetPagination
    basename = "residences"

    def get_queryset(self):
        user = self.request.user
        qs = Residence.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class CinViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = CinSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date_etablissement')
    pagination_class = StandardResultsSetPagination
    basename = "cin"

    def get_queryset(self):
        user = self.request.user
        qs = Cin.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class AmendeForfaitaireViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    serializer_class = AmendeForfaitaireSerializer
    permission_classes = PERMS
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unite', 'date')
    pagination_class = StandardResultsSetPagination
    basename = "amendes_forfaitaires"

    def get_queryset(self):
        user = self.request.user
        qs = AmendeForfaitaire.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)
