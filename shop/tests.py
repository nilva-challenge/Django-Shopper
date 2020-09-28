from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Items, Orders

SHOP_ORDER_URL = reverse('shop-api:list-create-order')
SHOP_ITEM_LIST_URL = reverse('shop-api:list-item')

USER_MODEL = get_user_model()


def create_user(**params):
    return USER_MODEL.objects.create_user(**params)


class PublicShopApiTests(TestCase):
    """Test the shop API (private)"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**{
            'email': 'test@pass.com',
            'password': "test_test",
            'first_name': 'test_name'
        })

        self.item = Items.objects.create(**{
            'name': 'car',
            'price': 25900,
            'amount': 50
        })

        self.client.force_authenticate(user=self.user)

    def test_create_valid_order_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'amount': 5,
            'user': self.user.id,
            'item': self.item.id,

        }
        res = self.client.post(SHOP_ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_order(self):
        """Test creating order with order amount more than required"""
        payload = {
            'amount': 500,
            'user': self.user.id,
            'item': self.item.id,

        }
        res = self.client.post(SHOP_ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_success(self):
        """Test get orders of the user"""

        res = self.client.get(SHOP_ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_items_success(self):
        """Test get items"""

        res = self.client.get(SHOP_ITEM_LIST_URL)

        self.assertEqual(res.data[0]['id'], self.item.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
