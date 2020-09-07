from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

LOGIN_URL = reverse('login')


class TestUsers(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        """Test that creating a user that doesn't exists"""
        payload = {"email": "test@test.com", "password": "test123"}

        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(payload["email"], str(response.data))

    def test_login_user(self):
        """Test request with exited user"""
        user = User.objects.create_user(email="test@test.com", password='test123')

        payload = {"email": "test@test.com", "password": "test123"}

        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=user)
        self.assertEqual(response.data.get('token'), token.key)

    def test_invalid_user_email(self):
        """Test request with invalid email address"""
        payload = {"email": "testcasdom", "password": "test123"}

        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
