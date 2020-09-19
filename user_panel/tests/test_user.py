from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

LOGIN_USER_URL = reverse('user:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(APITestCase):
    """Test the user api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_new_user_login(self):
        """Test login with new user is successful"""
        payload = {
            'email': 'mr.amirhossein1836@gmail.com',
            'password': 'Amir1376'
        }
        res = self.client.post(LOGIN_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_new_user_login_with_invalid_password(self):
        """Test login with invalid password failed"""
        payload = {
            'email': 'mr.amirhossein1836@gmail.com',
            'password': 'Am76'
        }
        res = self.client.post(LOGIN_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='mr.amirhossein1836@gmail.com',
            password='Pass.123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_user_login(self):
        """Test login exists user is successful"""
        payload = {
            'email': 'mr.amirhossein1836@gmail.com',
            'password': 'Pass.123'
        }
        res = self.client.post(LOGIN_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_user_login_with_invalid_password(self):
        """Test login exists user is successful"""
        payload = {
            'email': 'mr.amirhossein1836@gmail.com',
            'password': 'Pass.1234'
        }
        res = self.client.post(LOGIN_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
