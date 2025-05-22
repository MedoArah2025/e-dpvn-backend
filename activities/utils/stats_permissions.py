# activities/utils/stats_permissions.py

from rest_framework.exceptions import PermissionDenied

def can_access_unit_stats(user, unit_id):
    """
    Retourne True si l'utilisateur a accès aux stats de l'unité donnée.
    """
    if user.is_superuser:
        return True
    if hasattr(user, "role") and user.role in ("admin", "direction"):
        return True
    # Vérifie que l'utilisateur est bien de cette unité
    return str(getattr(user, "unite_id", "")) == str(unit_id)

def check_access_or_403(user, unit_id):
    """
    Lève 403 si l'utilisateur ne peut pas accéder à cette unité.
    """
    if not can_access_unit_stats(user, unit_id):
        raise PermissionDenied("Vous ne pouvez accéder qu'aux statistiques de votre unité.")
