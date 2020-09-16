from django.db import models

from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_set")
    count = models.IntegerField()

    order_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product.count -= self.count
        self.product.save()
        return super(Order, self).save(*args, kwargs)

    def __str__(self):
        return f"Order ID #{self.id}, Product: {self.product.title}"
