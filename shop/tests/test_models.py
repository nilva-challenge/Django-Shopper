from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import OrderItem, Order, Product
from django.utils import timezone

User = get_user_model()


class TestModels(TestCase):

    def test_product_model(self):
        """Test that create an instance of product works fine"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        self.assertEqual(str(product), product.name)

    def test_order_model(self):
        """Test that create an instance of order works fine"""
        user = User.objects.create_user(email="test@test.com", password="test123")
        order = Order.objects.create(ordered=timezone.now(), customer=user)
        self.assertEqual(str(order), "Order " + str(order.id))

    def test_order_item_model(self):
        """Test that create an instance of OrderItem works fine"""
        user = User.objects.create_user(email="test@test.com", password="test123")
        order = Order.objects.create(ordered=timezone.now(), customer=user)
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)
        self.assertEqual(str(order_item), str(order_item.id))
