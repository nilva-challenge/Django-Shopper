from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import OrderItem, Order, Product
from ..serializers import ProductSerializer

User = get_user_model()

PRODUCT_URL = reverse('shop:product-list')


def product_detail_url(product_id):
    """Return product detail URL"""
    return reverse('shop:product-detail', args=[product_id])


class TestProducts(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@email.com', password='test123')
        self.admin = User.objects.create_superuser(email='superuser@email.com', password='test123')

    def test_product_list_anonymous_user(self):
        """Test get list of products with anonymous user"""
        Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)

        response = self.client.get(PRODUCT_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_list_authenticated_user(self):
        """Test get list of product with authenticated user"""
        Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        self.client.force_authenticate(self.user)
        response = self.client.get(PRODUCT_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(serializer.data), len(response.data))
        self.assertEqual(serializer.data, response.data)

    def test_retrieve_list_anonymous_user(self):
        """Test retrieve a products with anonymous user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        Product.objects.create(name="Test 2", in_stock=4, description="Some text", price=12000)

        url = product_detail_url(product.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_retrieve_authenticated_user(self):
        """Test retrieve a product with authenticated user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        self.client.force_authenticate(self.user)

        url = product_detail_url(product.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], product.name)

    def test_create_product_with_user(self):
        """Test create a user with normal user"""
        payload = {"name": "P1", "in_stock": 5, "description": "Some text", "price": 120000}

        self.client.force_authenticate(self.user)
        response = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_admin(self):
        """Test create a user with admin user"""
        payload = {"name": "P1", "in_stock": 5, "description": "Some text", "price": 120000}

        self.client.force_authenticate(self.admin)
        response = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_partial_update_product_with_user(self):
        """Test partial update PATCH a user with normal user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        payload = {"name": "Updated Product", "in_stock": 10}

        self.client.force_authenticate(self.user)
        url = product_detail_url(product.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_product_with_admin(self):
        """Test partial update PATCH  a user with admin user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        payload = {"name": "Updated Product", "in_stock": 10}

        self.client.force_authenticate(self.admin)
        url = product_detail_url(product.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload["name"])
        self.assertEqual(response.data['in_stock'], payload["in_stock"])

    def test_full_update_product_with_user(self):
        """Test full update PUT a user with normal user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        payload = {"name": "Updated Product", "in_stock": 10, "description": "Some text", "price": 120000}

        self.client.force_authenticate(self.user)
        url = product_detail_url(product.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_product_with_admin(self):
        """Test full update PUT a user with admin user"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)
        payload = {"name": "Updated Product", "in_stock": 10, "description": "Some text", "price": 120000}

        self.client.force_authenticate(self.admin)
        url = product_detail_url(product.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload["name"])
        self.assertEqual(response.data['in_stock'], payload["in_stock"])
        self.assertEqual(response.data['description'], payload["description"])
        self.assertEqual(response.data['price'], payload["price"])

    def test_delete_product(self):
        """Test delete product"""
        product = Product.objects.create(name="Test", in_stock=4, description="Some text", price=12000)

        self.client.force_authenticate(self.admin)
        url = product_detail_url(product.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
