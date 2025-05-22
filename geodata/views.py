from rest_framework import viewsets, permissions
from .models import Quartier
from .serializers import QuartierSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    - Lecture pour tous (GET, HEAD, OPTIONS)
    - Création/modification/suppression pour admin uniquement
    """
    def has_permission(self, request, view):
        # Méthodes "safe" = lecture seule
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin Django ou utilisateur avec rôle admin
        user = request.user
        return (
            user and user.is_authenticated and
            (user.is_superuser or getattr(user, "role", None) == "admin")
        )

class QuartierViewSet(viewsets.ModelViewSet):
    queryset = Quartier.objects.all().order_by("nom")
    serializer_class = QuartierSerializer
    permission_classes = [IsAdminOrReadOnly]


