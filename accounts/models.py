from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    Modified User model for using email address as username.
    """
    username = None
    email = models.EmailField(_("Email Address"), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Profile(models.Model):
    """
    User's Profile Model
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.fullname:
            return self.fullname
        else:
            return self.user.email
