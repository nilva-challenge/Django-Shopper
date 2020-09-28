from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

"""related_name protocol for foreignKey
<from table name>_<to table name> """


class EmailUserManager(UserManager):
    def _create_user(self, email, password, username, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, username, **extra_fields)


class EmailUser(AbstractUser):
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE, null=False, blank=False, related_name="user_site",
                             default=settings.SITE_ID)

    email = models.EmailField(
        _('email'),
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        blank=True, null=True,
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_email_verified = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.email.lower()

    objects = EmailUserManager()

