# geodata/urls.py
from rest_framework.routers import DefaultRouter
from .views import QuartierViewSet

router = DefaultRouter()
router.register(r'quartiers', QuartierViewSet, basename='quartier')

urlpatterns = router.urls
