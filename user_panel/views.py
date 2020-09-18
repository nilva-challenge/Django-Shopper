from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework import status
from . import serializers
import requests
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Function for receive token from JWT"""

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLoginApiView(generics.CreateAPIView):
    """User login"""
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        try:
            get_user_model().objects.get(email=email)
            user = authenticate(email=email, password=password)
            if user is not None:
                res = get_tokens_for_user(user)
                return Response(
                    res,
                    status=status.HTTP_200_OK
                )
            else:
                res = {
                    'error': 'The provided credentials are not valid'
                }
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except get_user_model().DoesNotExist:
            if len(password) < 8:
                res = {
                    'error': 'The length of password must be more than 8'
                }
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = get_user_model().objects.create_user(email=email, password=password)
                res = get_tokens_for_user(user)
                return Response(
                    res,
                    status=status.HTTP_201_CREATED
                )
