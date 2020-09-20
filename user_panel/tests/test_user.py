from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from user_panel import serializers

# urls
LOGIN_USER_URL = reverse('user:login')
ME_URL = reverse('user:me')


def create_user(**params):
    """
        Create new user
    """
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

    def test_user_profile_for_unauthorized_user(self):
        """Test that unauthorized user can't see any profile"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_retrieve_user_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        user = get_user_model().objects.get(id=self.user.id)

        serializer = serializers.UserEditSerializer(user, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""

        payload = {
            'name': 'Joel',
            'password': 'Amoi928.dish'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
