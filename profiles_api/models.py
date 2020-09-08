from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email')
        email = self.normalize_email(email=email)  # Normalizes email addresses by lowercasing the domain portion of the email address.
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)  # set_password for encrypting password (hash password)
        user.save(using=self._db)  # if django has multiple database
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """Creates and saves a superuser with the given email, date of"""
        user = self.create_user(email=email, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


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
