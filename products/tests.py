from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from products.models import Product
from products.serializers import ProductSerializer
from products.api import ProductListAPI

from accounts.models import CustomUser


class TestProductListEndpoint(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view =ProductListAPI.as_view()

        self.product_1 = Product.objects.create(title="Test 01", price=2.3, count=2)
        self.product_2 = Product.objects.create(title="Test 02", price=2.3, count=1)
        self.product_3 = Product.objects.create(title="Test 03", price=2.3, count=0)

        self.test_user = CustomUser.objects.create_user(email="test@gmail.com", password="123")
        self.token = Token.objects.create(user=self.test_user)
    
    def test_invalid_get(self):
        """
        Tests not authenticated request
        """
        response = self.client.get(
            reverse("products_api")
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_valid_get(self):
        """
        Tests authenticated request
        """
        request = self.factory.get(
            reverse("products_api"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ProductSerializer(
                instance=[self.product_1, self.product_2], many=True
                ).data
            )
