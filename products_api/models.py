from django.db import models
from profiles_api.models import User
from django.db.models.signals import post_save


class Product(models.Model):
    """Database model for products"""
    name = models.CharField(max_length=500)
    count = models.PositiveIntegerField(default=1, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    available = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)  # when change object this field update

    class Meta:
        ordering = ('name',)  # order base on name alphabet

    def __str__(self):
        return self.name

    def check_remaind_count(self, count):
        """chack if the customer can order or not"""
        if self.count - count >= 0:
            return True
        else:
            return False

    def change_availble_count(self, count):
        """change availalble if there is no any capaccity and change count of product after any order"""
        self.count = self.count - count
        if self.available == False:
            pass
        else:
            if self.count == 0:

                self.available = False
            else:
                pass
        self.save()


class OrderItem(models.Model):
    """Database model for order items"""
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    count = models.PositiveIntegerField(blank=False, null=False, default=1)

    def __str__(self):
        return f'name : {self.product_id.name} / counts : {self.count} '


class Order(models.Model):
    """Database model for order that is related to orderitem"""
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'customer_email : {self.customer_id.email}'


def change_availble(sender, instance, created, **kwargs):
    """If instance create changes occur in the database"""
    if created:
        obj = Product.objects.get(id=instance.product_id.id)
        Product.change_availble_count(obj, count=instance.count)


# (Signal) after creating orderItem record ,count of product change and If the count of product is ended, the available filed will be zero
post_save.connect(change_availble, sender=OrderItem)
