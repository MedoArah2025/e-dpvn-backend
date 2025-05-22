# core/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from accounts.views import UserViewSet
from units.views import (
    UniteViewSet,
    ActivityGroupViewSet,
    UniteActivityGroupViewSet,
)
from activities.urls import router as activities_router
from activities.views.stats import StatisticsByUnitView, StatisticsGlobalView
from activities.views.export_stats import ExportStatsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from geodata.views import QuartierViewSet
from activities.views.stats import StatisticsGlobalFlatView
from geodata.urls import router as geodata_router

# Routeur principal DRF
router = DefaultRouter()
router.register(r'users',           UserViewSet,               basename='user')
router.register(r'units',           UniteViewSet,              basename='unit')
router.register(r'activity-groups', ActivityGroupViewSet,      basename='activitygroup')
router.register(r'unit-groups',     UniteActivityGroupViewSet, basename='unitgroup')
router.register(r'units/quartiers', QuartierViewSet, basename="quartier")

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # API v1: comptes, unités, groupes, ...
    path('api/', include(router.urls)),

    # API v1: activités (toutes les ViewSets de activities/urls.py)
    #path('api/activities/', include(activities_router.urls)),
    path('api/activities/', include('activities.urls')),

    # Auth JWT
    path('api/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # OpenAPI / Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',   SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Statistiques par unité
    path(
        'api/statistics/units/<int:unit_id>/',
        StatisticsByUnitView.as_view(),
        name='statistics-by-unit'
    ),
    # Export Excel des stats par unité
    path(
        'api/statistics/units/<int:unit_id>/export/',
        ExportStatsView.as_view(),
        name='export-statistics'
    ),
    # Statistiques globales
    path(
        'api/statistics/global/',
        StatisticsGlobalView.as_view(),
        name='statistics-global'
    ),
path(
    'api/statistics/global/flat/',
    StatisticsGlobalFlatView.as_view(),
    name='statistics-global-flat'
),

    path('api/geodata/', include(geodata_router.urls)),
    path('api/auth/', include('accounts.urls')),

]
