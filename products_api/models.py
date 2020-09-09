from django.db import models
from profiles_api.models import UserProfile
from datetime import datetime


class Product(models.Model):
    """Database model for products"""
    name = models.CharField(max_length=500)
    count = models.PositiveIntegerField(default=1, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    create_date = models.DateTimeField(blank=False, default=datetime.now)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Database model for orders of users"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(blank=False, null=False)
    order_date = models.DateTimeField(default=datetime.now, blank=False, null=False)

    def __str__(self):
        return self.product
