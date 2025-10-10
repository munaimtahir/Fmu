from rest_framework.permissions import BasePermission, SAFE_METHODS

def in_group(user, group_name: str) -> bool:
    try:
        return user.groups.filter(name=group_name).exists()
    except Exception:
        return False

class IsAdminOrRegistrarReadOnlyFacultyStudent(BasePermission):
    """
    Admin/Registrar: full access.
    Faculty/Student: read-only (SAFE methods). Refine per-module if needed.
    """
    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser or in_group(u, "Admin") or in_group(u, "Registrar"):
            return True
        return request.method in SAFE_METHODS
