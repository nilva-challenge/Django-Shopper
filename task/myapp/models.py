from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    available = models.IntegerField()

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, default=0)
