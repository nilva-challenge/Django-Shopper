from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from accounts.models import CustomUser
from accounts.api import ProfileAPI, LoginAPI


class TestLoginEndpoint(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LoginAPI.as_view()

        self.test_user = CustomUser.objects.create_user("test@gmail.com", "123")
        self.test_user.save()

        self.token = Token.objects.create(user=self.test_user)
        self.token.save()
    
    def test_valid_token(self):
        """
        Tests if token is valid
        """
        response = self.client.post(
            reverse("login_api"),
            data={"email": self.test_user.email, "password": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('token'), self.token.key)
    
    def test_invalid_credentials(self):
        """
        Tests if credentials are invalid
        """
        response = self.client.post(
            reverse("login_api"),
            data={"email": self.test_user.email, "password": "1234"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('password'), ["Password is not correct."])



class TestProfileEndpoint(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileAPI.as_view()

        self.test_user = CustomUser.objects.create_user("test@gmail.com", "123")
        self.test_user.profile.age = 22
        self.test_user.profile.save()
        
        self.token = Token.objects.create(user=self.test_user)
        self.token.save()
    
    def test_invalid_get(self):
        """
        Tests not authenticated request
        """
        response = self.client.get(reverse('profile_api'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_valid_get(self):
        """
        Tests authenticated request
        """
        request = self.factory.get(
            reverse('profile_api'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
            )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 22)
    
    def test_valid_patch(self):
        """
        Tests the function of patch request
        """
        request = self.factory.patch(
            reverse('profile_api'),
            data={"age": 32, "fullname": "Test Name"},
            format="json",
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
            )
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 32)
        self.assertEqual(response.data['fullname'], "Test Name")
