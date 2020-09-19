from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

PRODUCT_LIST_URL = reverse('shop:products')
ORDER_PRODUCT_URL = reverse('shop:order')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicShopApiTest(APITestCase):
    """Test the shop API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_product_list_by_unauthorized_user(self):
        """Test that product list doesn't show for unauthorized user"""

        res = self.client.get(PRODUCT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_product_by_unauthorized_user(self):
        """Test that ordering products doesn't work for unauthorized user"""

        res = self.client.post(ORDER_PRODUCT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShopApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='mr.amirhossein1836@gmail.com',
            password='Pass.123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_product_list(self):
        """Test that authorized user can get products"""

        res = self.client.post()