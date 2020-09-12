from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, password, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email')
        email = self.normalize_email(email=email)  # Normalizes email addresses by lowercasing the domain portion of the email address.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # set_password for encrypting password (hash password)
        user.save(using=self._db)  # if django has multiple database
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with the given email, date of"""
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
