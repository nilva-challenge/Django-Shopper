from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive_float(value):
    """
        this validator check price be positive
    """
    if value < 0:
        raise ValidationError(
            _('%(value)s is lower than zero'),
            params={'value': value},
        )


class UserManager(BaseUserManager):
    """
        manager for user model
    """
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""

        if not email:
            raise ValueError('Users must have an email address')

        # normalize email
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.FloatField(validators=[validate_positive_float])

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    price = models.FloatField(validators=[validate_positive_float])
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}, {self.user.email}'

    # this is for list order item related to current order obj
    @property
    def order_items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order.id}, {self.product.name}'
