from django.db import models

from products.managers import ProductManager


class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)

    objects = ProductManager()

    def __str__(self):
        return self.title
