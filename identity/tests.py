from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from rest_framework.authtoken.models import Token

User = get_user_model()


class UserEmailLoginTests(APITestCase):
    def setUp(self):
        # Replace with the actual URL name
        self.login_url = reverse('email_login')
        # Replace with the actual URL name
        self.password_login_url = reverse('password_login')
        self.client = APIClient()

    def test_user_email_login(self):
        # Create a test user
        user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword1234')

        # Prepare data for email login
        email_data = {'email': 'testuser@example.com'}

        # Make a POST request to initiate email login
        response = self.client.post(self.login_url, email_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Check if the redirection URL contains the email parameter
        expected_redirect_url = f'{self.password_login_url}?email={email_data["email"]}'
        self.assertEqual(response.url, expected_redirect_url)

    def test_invalid_email_login(self):
        # Prepare invalid email data
        invalid_email_data = {'email': 'invalidemail'}

        # Make a POST request with invalid email data
        response = self.client.post(self.login_url, invalid_email_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPasswordLoginViewTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword1234',
        }

        # Creating a user with a hashed password
        self.user = User.objects.create(
            email=self.user_data['email'],
            password=make_password(self.user_data['password']),
        )

        self.login_url = reverse('password_login')

    def test_get_user_email(self):
        response = self.client.get(
            self.login_url, {'email': self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_successful_password_login(self):
        login_data = {
            'password': self.user_data['password'],
        }

        self.password_login_url = f'{self.login_url}?email={self.user_data["email"]}'
        response = self.client.post(self.password_login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_password(self):
        login_data = {
            'password': 'wrongpassword',
        }

        self.password_login_url = f'{self.login_url}?email={self.user_data["email"]}'
        response = self.client.post(self.password_login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid password')

    def test_user_creation_on_nonexistent_user(self):
        non_existent_email = 'nonexistent@example.com'
        login_data = {
            'password': self.user_data['password'],
        }

        self.password_login_url = f'{self.login_url}?email={non_existent_email}'
        response = self.client.post(self.password_login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Check if a new user has been created in the database
        new_user = User.objects.get(email=non_existent_email)
        self.assertIsNotNone(new_user)


class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword1234',
        }

        self.user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['email'],
            password=self.user_data['password']
        )

        # Creating a token for the user
        self.token = Token.objects.create(user=self.user)

        self.profile_url = reverse('profile')

    def test_retrieve_user_profile(self):
        # Set authentication header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_update_user_profile(self):
        # Set authentication header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        updated_data = {
            'email': 'updated@example.com',
        }

        response = self.client.patch(self.profile_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the user instance from the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data['email'])

    def test_unauthenticated_access(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
