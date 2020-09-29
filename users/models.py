from django.db import models

# Create your models here.


# from django.contrib.auth.models import User as AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

from django.conf import settings


class User(AbstractUser):
    # username = models.CharField(_('username'), max_length=150, blank=True, null=True,default="")
    username = None
    address = models.CharField(max_length=300, default="", blank=True, null=True)
    postal_code = models.CharField(max_length=15, default="", blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    # user = models.ForeignKey(User, blank=True, null=True, default="" ,on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default="", on_delete=models.SET_NULL)
    key = models.CharField(max_length=100, unique=True)
    last_login_date = models.DateField(
        verbose_name='last login date', auto_now_add=True)

    def __str__(self):
        return '{}_{}'.format(str(self.key), str(self.user.first_name + " " + self.user.last_name))
