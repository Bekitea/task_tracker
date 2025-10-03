from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        return request.user.groups.filter(name='admins').exists()