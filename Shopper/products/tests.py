from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import product, Order, OrderItem
from rest_framework import status
from rest_framework.authtoken.models import Token
import json


class ProductTest(APITestCase):
    def setUp(self):
        # Creates two products and user
        self.test_product1 = product.objects.create(name="product1", quantity=5, is_available=True)
        self.test_product2 = product.objects.create(name="prodcute2", quantity=10, is_available=False)

        self.user = User.objects.create_user(username='user@foo.com', email='user@foo.com', password='top_secret')

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        # URL for getting the available products
        self.create_url = reverse('products-list')

    def test_products_list(self):

        expected_result = [
            {
                "name": "product1",
                "quantity": 5
            }
        ]

        response = self.client.get(self.create_url, HTTP_AUTHORIZATION='Token {}'.format(self.token), format='json')
        # Checks if response is equal to expected result
        output_dict = json.loads(json.dumps(response.data))

        self.assertEqual(output_dict, expected_result)


class OrderTest(APITestCase):

    def setUp(self):
        # Creates two products
        self.test_product1 = product.objects.create(name='test_product1', quantity=5)
        self.test_product1 = product.objects.create(name='test_product2', quantity=5)

        self.user = User.objects.create_user(username='user@foo.com', email='user@foo.com', password='top_secret')

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.create_url = reverse('order')

    def test_order(self):
        data = [
            {
                "product": 1,
                "quantity": 4
            },
            {
                "product": 2,
                "quantity": 3
            }
        ]
        response = self.client.post(self.create_url, data=data, HTTP_AUTHORIZATION='Token {}'.format(self.token), format='json')
        # Checks the status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checks if order is created
        self.assertEqual(Order.objects.count(), 1)
