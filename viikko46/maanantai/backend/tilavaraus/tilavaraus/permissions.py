from rest_framework.permissions import BasePermission

class IsUserOrReadOnly(BasePermission):
    """
    Allow 'user' role to view records and create reservations.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Admins can do anything
            if request.user.rooli == 'admin':
                return True
            # Users can only perform 'GET' (view records) and 'POST' (create reservations)
            if request.method in ['GET', 'POST'] and request.user.rooli == 'user':
                return True
        return False


class IsAdminUser(BasePermission):
    """
    Allow 'admin' role full CRUD access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rooli == 'admin'
