from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrNoDeleteForDirectionOrAgent(BasePermission):
    """
    Permissions personnalisées :
    - Admin : tous droits (lecture, création, modification, suppression)
    - Direction et Agent : lecture, création, modification (GET, POST, PUT, PATCH)
                           PAS de suppression (DELETE interdit)
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, 'role', None) == "admin":
            return True
        # Permet GET, HEAD, OPTIONS (SAFE_METHODS) + POST/PUT/PATCH
        if request.method in SAFE_METHODS or request.method in ['POST', 'PUT', 'PATCH']:
            return True
        # Interdit DELETE (ou toute autre méthode non listée)
        return False

    def has_object_permission(self, request, view, obj):
        # Même logique au niveau objet
        return self.has_permission(request, view)
