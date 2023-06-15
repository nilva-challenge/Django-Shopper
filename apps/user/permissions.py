from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class IsSellerUser(BasePermission):
    """
        Allow Seller for use Actions
    """
    message = _("Only Sellers can Access")

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role == User.RoleChoices.SELLER
        )


class IsAdminUser(BasePermission):
    """
        Allow Admin for use Actions
    """
    message = _("Only Admin can Access")

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role == User.RoleChoices.ADMIN
        )


class IsCustomerUser(BasePermission):
    """
        Allow Admin for use Actions
    """
    message = _("Only Admin can Access")

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role == User.RoleChoices.CUSTOMER
        )
