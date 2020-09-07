from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

User = get_user_model()


def get_profile_url(user_id):
    return reverse('user-detail', args=[user_id])


class PublicUserProfileTests(TestCase):

    def test_auth_required(self):
        """Test that authentication is required"""
        user = User.objects.create_user(email='testuser@email.com', password='test123')
        url = get_profile_url(user.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserProfileTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='testuser@email.com', password='test123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=Token.objects.get_or_create(user=self.user))

    def test_retrieve_user_profile(self):
        """Test retrieving other users profiles """
        other_user = User.objects.create_user(email='testuser1@email.com', password='test123')
        url = get_profile_url(other_user.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_limited_to_user(self):
        """Test that a user can't update other user profile"""
        payload = {"first_name": "Test name"}
        other_user = User.objects.create_user(email='testuser1@email.com', password='test123')
        url = get_profile_url(other_user.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update(self):
        """Test user update her/his profile with PATCH"""
        payload = {"first_name": "Test name"}
        url = get_profile_url(self.user.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], payload["first_name"])

    def test_full_update(self):
        """Test user update her/his profile with put"""
        payload = {"first_name": "Test first", "last_name": "Test last", "email": "another@email.com",
                   "date_of_birth": "1996-02-14"}
        url = get_profile_url(self.user.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], payload["first_name"])
        self.assertEqual(response.data['last_name'], payload["last_name"])
        self.assertEqual(response.data['email'], payload["email"])
        self.assertEqual(response.data['date_of_birth'], payload["date_of_birth"])
