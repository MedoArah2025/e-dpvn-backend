# activities/views/spja.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsAdminOrNoDeleteForDirectionOrAgent
from activities.models.spja import MiseADispositionSpja
from activities.serializers.spja import MiseADispositionSpjaSerializer

PERMS = [IsAuthenticated, IsAdminOrNoDeleteForDirectionOrAgent]

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class MiseADispositionSpjaViewSet(viewsets.ModelViewSet):
    serializer_class = MiseADispositionSpjaSerializer
    permission_classes = PERMS
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["unite", "date_mise"]
    ordering_fields = ["date_mise", "unite"]
    pagination_class = StandardResultsSetPagination
    basename = "mise_a_disposition_spja"

    def get_queryset(self):
        user = self.request.user
        qs = MiseADispositionSpja.objects.all()
        if user.role in ["admin", "direction"]:
            return qs
        return qs.filter(unite=user.unite)
