from rest_framework import permissions


class AdminUpdateProduct(permissions.BasePermission):
    """Allow admin user that to create update and other changes in product,only user that authorized can see all of product"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        elif request.method not in permissions.SAFE_METHODS and request.user.is_staff:
            return True
        else:
            return False
