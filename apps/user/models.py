from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.managers import CustomUserManager


class User(AbstractUser):
    class RoleChoices(models.IntegerChoices):
        ADMIN = 1, _('admin')
        CUSTOMER = 2, _('customer')
        SELLER = 3, _('seller')

    role = models.PositiveSmallIntegerField(_('role'), choices=RoleChoices.choices, default=RoleChoices.ADMIN)
    email = models.EmailField(_("email address"), unique=True)
    REQUIRED_FIELDS = ("first_name",)
    USERNAME_FIELD = "email"
    username = None
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("users")
        verbose_name = _("user")
        db_table = "user"
