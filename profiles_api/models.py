from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    pass


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # this field for access to django admin
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        """Return string of users"""
        return self.email
