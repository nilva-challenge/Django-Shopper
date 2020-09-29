from django.db import models

from users.models import User


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام محصول")
    stock = models.IntegerField(verbose_name="موجودی انبار")
    price = models.IntegerField(verbose_name="قیمت")

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProductRelation')

    def __str__(self):
        return self.user


class OrderProductRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_number = models.IntegerField()
    unit = models.IntegerField()
