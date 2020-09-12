from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """permission for admin user"""

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwner(permissions.BasePermission):
    """permission for admin user and user that is login can edit his/her profile"""

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.id == request.user.id
        else:
            return False
