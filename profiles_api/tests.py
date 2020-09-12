from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class MemberTests(APITestCase):
    def test_api_jwt(self):
        url = reverse('profiles_api:login_user')
        resp = self.client.post(url, {'email': 'ali@gmail.com', 'password': '8812621012'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
