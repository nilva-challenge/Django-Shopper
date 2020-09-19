from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from core import models
from shopper import serializers

PRODUCT_LIST_URL = reverse('shop:products')
ORDER_PRODUCT_URL = reverse('shop:order')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_product(name, **params):
    """Create and return a sample product"""
    defaults = {
        'stock': 10,
        'price': 5.00
    }
    defaults.update(params)

    return models.Product.objects.create(name=name, **defaults)


def sample_order(user, price=0):
    """Create and return a sample order"""

    return models.Order.objects.create(user=user, price=price)


def sample_order_item(order, product, quantity):
    """Create and return a sample order item"""

    return models.OrderItem.objects.create(order=order, product=product, quantity=quantity)


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
        """Test that user can get products"""
        sample_product('pro max')
        sample_product('11 pro max')

        res = self.client.get(PRODUCT_LIST_URL)

        products = models.Product.objects.all()

        serializer = serializers.ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_products_list_with_unavailable_product(self):
        """Test that API only show available products"""

        sample_product('pro max', stock=0)
        sample_product('11 pro max')

        res = self.client.get(PRODUCT_LIST_URL)

        products = models.Product.objects.filter(stock__gt=0)

        serializer = serializers.ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_ordering_product_successful(self):
        """Test that ordering products with correct payload is successful"""
        pro1 = sample_product('pro max')
        pro2 = sample_product('note 10')
        pro3 = sample_product('mi 10')

        order = sample_order(self.user)

        sample_order_item(order, pro1, 4)
        sample_order_item(order, pro2, 2)
        sample_order_item(order, pro3, 3)

        payload = [
            {
                'id': pro1.id,
                'quantity': 4
            },
            {
                'id': pro2.id,
                'quantity': 2
            },
            {
                'id': pro3.id,
                'quantity': 3
            },
        ]
        res = self.client.post(ORDER_PRODUCT_URL, {
            'products':payload
        })

        serializer = serializers.OrderSerializer(order, many=False)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        # self.assertEqual(len(res.data), 1)