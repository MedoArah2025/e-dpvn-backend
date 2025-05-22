from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.utils.excel_mixin import ExcelExportMixin
from activities.models.dispositions import (
    MiseslctCto,
    MiseDPJ,
    MiseDispositionOcrit,
    MiseDispositionDouane,
    MiseDST,
    MiseDPMF,
    MisePavillonE,
    MiseSoniloga,
)
from activities.serializers.dispositions import (
    MiseslctCtoSerializer,
    MiseDPJSerializer,
    MiseDispositionOcritSerializer,
    MiseDispositionDouaneSerializer,
    MiseDSTSerializer,
    MiseDPMFSerializer,
    MisePavillonESerializer,
    MiseSonilogaSerializer,
)

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class BaseDispositionViewSet(ExcelExportMixin, viewsets.ModelViewSet):
    """
    CRUD des mesures de disposition.

    - Filtrable par unité et date de mise.
    - Tri possible sur la date de mise et l'unité.
    - Pagination standard (20 items par page).
    - GET /api/dispositions/<resource>/export/ → export Excel
    """
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_mise"]
    ordering_fields = ["date_mise", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "disposition"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)

class MiseslctCtoViewSet(BaseDispositionViewSet):
    queryset = MiseslctCto.objects.all()
    serializer_class = MiseslctCtoSerializer
    basename = "slct_cto"

class MiseDPJViewSet(BaseDispositionViewSet):
    queryset = MiseDPJ.objects.all()
    serializer_class = MiseDPJSerializer
    basename = "dpj"

class MiseDispositionOcritViewSet(BaseDispositionViewSet):
    queryset = MiseDispositionOcrit.objects.all()
    serializer_class = MiseDispositionOcritSerializer
    basename = "ocr_im"

class MiseDispositionDouaneViewSet(BaseDispositionViewSet):
    queryset = MiseDispositionDouane.objects.all()
    serializer_class = MiseDispositionDouaneSerializer
    basename = "douane"

class MiseDSTViewSet(BaseDispositionViewSet):
    queryset = MiseDST.objects.all()
    serializer_class = MiseDSTSerializer
    basename = "dst"

class MiseDPMFViewSet(BaseDispositionViewSet):
    queryset = MiseDPMF.objects.all()
    serializer_class = MiseDPMFSerializer
    basename = "dpmf"

class MisePavillonEViewSet(BaseDispositionViewSet):
    queryset = MisePavillonE.objects.all()
    serializer_class = MisePavillonESerializer
    basename = "pavillon_e"

class MiseSonilogaViewSet(BaseDispositionViewSet):
    queryset = MiseSoniloga.objects.all()
    serializer_class = MiseSonilogaSerializer
    basename = "soniloga"
