from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email="mr.amirhossein1836@gmail.com", password="Pass.123"):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "mr.amirhossein1836@gmail.com"
        password = "Pass.123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """Test user email is normalized"""
        email = 'mr.amirhossein1836@GMAIL.com'
        user = get_user_model().objects.create_user(
            email=email,
            password="Pass.123"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Pass.123')

    def test_create_new_superuser(self):
        """Test creating new super user"""
        user = get_user_model().objects.create_superuser(
            email='mr.amirhossein1836@gmail.com',
            password='Pass.123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_product_str(self):
        """Test the product string representation"""
        product = models.Product.objects.create(
            name='pro max',
            stock=5,
            price=1250
        )

        self.assertEqual(str(product), product.name)

    def test_order_str(self):
        """Test the order string representation"""
        order = models.Order.objects.create(
            user=sample_user(),
            price=0
        )

        self.assertEqual(str(order), order.user.email)

    def test_order_item_str(self):
        """Test the order item string representation"""
        order = models.Order.objects.create(
            user=sample_user(),
            price=0
        )
        product = models.Product.objects.create(
            name='pro max',
            stock=5,
            price=1250
        )
        order_item = models.OrderItem.objects.create(
            order=order,
            product=product,
            quantity=10
        )

        self.assertEqual(str(order_item), f'{order.id}, {product.name}')
