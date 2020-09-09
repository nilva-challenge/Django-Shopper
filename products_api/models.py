from django.db import models
from profiles_api.models import UserProfile
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=500)
    count = models.IntegerField(default=1, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    create_date = models.DateTimeField(blank=False, default=datetime.now)


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, null=False)
    order_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
