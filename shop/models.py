from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=1)

    @property
    def is_sold(self):
        """
        Property to check if the product is sold (available_quantity is zero).

        Returns:
        - bool: True if the product is sold, False otherwise.
        """
        return self.available_quantity == 0

    def __str__(self):
        return self.name


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        """
        Calculate the total price for the order.

        Returns:
        - Decimal: Total price for the order.
        """
        order_items = self.order_items.all()
        total_price = sum(item.subtotal() for item in order_items)
        return total_price

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """
        Calculate the subtotal price for the order item.

        Returns:
        - Decimal: Subtotal price for the order item.
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
