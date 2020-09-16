from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from orders.api import OrdersAPI
from orders.models import Order
from orders.serializers import OrderSerializer

from products.models import Product
from accounts.models import CustomUser


class TestOrdersAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = OrdersAPI.as_view()

        self.product_1 = Product.objects.create(title="Test 01", price=2.3, count=2)
        self.product_2 = Product.objects.create(title="Test 02", price=2.3, count=1)
        self.product_3 = Product.objects.create(title="Test 03", price=2.3, count=0)

        self.test_user = CustomUser.objects.create_user(email="test@gmail.com", password="123")
        self.token = Token.objects.create(user=self.test_user)
    
    def test_invalid_token(self):
        """
        Tests not authenticated post/get request
        """
        response = self.client.post(
            reverse("orders_api"),
            data={"product": 2, "count": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(
            reverse("orders_api")
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_valid_empty_get(self):
        """
        Tests authenticated empty result get request
        """
        request = self.factory.get(
            reverse("orders_api"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])
    
    def test_valid_post(self):
        """
        Tests true functionality of an order
        """
        request = self.factory.post(
            reverse("orders_api"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
            data = {"product": self.product_1.id, "count": 1}
        )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.product_1.count, 2)

        # Check to see order submitted in database or not
        request = self.factory.get(
            reverse("orders_api"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        
        expected_data = OrderSerializer(
            instance=Order.objects.all(), many=True
        ).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data, expected_data)

    
    def test_invalid_post(self):
        """
        Tests error function of an order
        """
        request = self.factory.post(
            reverse("orders_api"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
            data = {"product": self.product_1.id, "count": 1000}
        )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.product_1.count, 2)



        
