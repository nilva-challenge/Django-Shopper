from django.contrib.auth.models import User
from django.db import models


class product(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)


class Order(models.Model):
    costumer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(product, on_delete=models.CASCADE)

