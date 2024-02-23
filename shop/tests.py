from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *

User = get_user_model()


class ProductListCreateViewTests(APITestCase):
    def create_authenticated_user(self):
        """
        Helper method to create an authenticated user.
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=user)
        return user

    def setUp(self):
        self.user = self.create_authenticated_user()
        self.product_data = {
            'name': 'Test Product',
            'available_quantity': 4,
            'description': 'Test description',
            'price': 10
        }
        self.product = Product.objects.create(**self.product_data)
        self.url = '/api/products/'

    def test_create_product(self):
        response = self.client.post(self.url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_non_sold_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        serialized_data = ProductSerializer(
            instance=[self.product], many=True).data
        self.assertEqual(response.data['results'], serialized_data)


class OrderListCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com',
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='Test Description',
            available_quantity=5,
        )
        self.order_url = reverse('order_list_create')
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        data = {
            'order_items': [
                {
                    'product': self.product.id,
                    'quantity': 2,
                }
            ]
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Product.objects.get(
            id=self.product.id).available_quantity, 3)

    def test_create_order_insufficient_quantity(self):
        data = {
            'order_items': [
                {
                    'product': self.product.id,
                    'quantity': 10,  # This quantity exceeds available_quantity
                }
            ]
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(Product.objects.get(
            id=self.product.id).available_quantity, 5)

    def test_create_order_nonexistent_product(self):
        data = {
            'order_items': [
                {
                    'product': 999,  # Nonexistent product ID
                    'quantity': 2,
                }
            ]
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_get_order_list(self):
        Order.objects.create(user=self.user)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_get_order_list_empty(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
