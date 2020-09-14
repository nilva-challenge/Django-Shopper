from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from google.auth.transport import requests
from google.oauth2 import id_token

from accounts.serializers import LoginSerializer, ProfileSerializer
from accounts.utils import get_user, User
from accounts.models import Profile


class GoogleLoginAPI(APIView):
    """
    Login with information sent back from google!
    """
    def post(self, *args, **kwargs):
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        idinfo = id_token.verify_oauth2_token(self.request.data['code'], requests.Request(), client_id)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user = get_user(idinfo.get('email'))
        if user is None: 
            user = User.objects.create(email=idinfo.get('email'))
            user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class LoginAPI(APIView):
    def post(self, *args, **kwargs):
        """
        Authenticates and existing user or creates an account first if email does not exist.

        Returns:
            token with status code 200: a string containing auth token
            errors with status code 401 for wrong password or status code 400 for invalid inputs
        """
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        password = serializer.data.get('password')

        # Check if user exists
        user = get_user(serializer.data.get('email'))
        if user is None: 
            user = User.objects.create(email=email)
            user.save()
            user.set_password(password)
            user.save()
        user = authenticate(**serializer.data)
        if user:
            login(self.request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"password": ["Password is not correct.", ]}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileAPI(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileSerializer

    def get_queryset(self, **kwargs):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get(self, *args, **kwargs):
        data = self.serializer_class(instance=self.get_queryset()).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def put(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

