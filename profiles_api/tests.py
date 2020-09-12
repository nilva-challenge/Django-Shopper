from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.hashers import make_password

class MemberTests(APITestCase):
    def test_api_jwt(self):
        url = reverse('profiles_api:login_user')
        password =('8812621012')
        resp = self.client.post(url, {'email': '', 'password': password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
