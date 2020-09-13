from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('accounts-create')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 200 ok code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checks if the token saved in database
        self.assertEqual(response.data['token'], Token.objects.get(user=User.objects.get(email='foobar@example.com')).key)


class ProfileTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='user@foo.com', email='user@foo.com', password='top_secret', first_name = 'first_name', last_name = 'last_name')

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.create_url = reverse('profile')

    def test_create_user(self):
        # Tests if the profile returns correct
        expected_result = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "user@foo.com",
            "username": "user@foo.com"
        }
        response = self.client.get(self.create_url, HTTP_AUTHORIZATION='Token {}'.format(self.token), format='json')
        self.assertEqual(expected_result, response.data)

        # Tests if profile edits is ok
        data = {
            "first_name": "first_name2",
            "last_name": "last_name2",
            "email": "user@foo.com",
            "username": "user@foo.com"
        }
        response = self.client.put(self.create_url, data=data, HTTP_AUTHORIZATION='Token {}'.format(self.token), format='json')
        self.assertEqual(data, response.data)