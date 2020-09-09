from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from .permissions import UserIsOwnerOrReadOnly
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.urls import reverse
from dj_rest_auth.registration.views import SocialLoginView

from django.shortcuts import redirect
import urllib.parse

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPIView(CreateAPIView):
    """Login existing user and sign up new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"User Created with email: ": serializer.data.get('email')}, status=status.HTTP_201_CREATED,
                            headers=headers)
        elif User.objects.filter(email=request.data.get('email')).exists():
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            else:
                return Response({"Message": "Email or Password is wrong!"})
        else:
            return Response({"Error": "Check your fields"}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data.get('password')))


class GoogleLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    # callback_url = 'http://localhost:8000/api/users/auth/google/login/callback/'
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('google_callback'))


def google_callback(request):
    params = urllib.parse.urlencode(request.GET)
    print("-------------------------------------------")
    print(params)
    print("-------------------------------------------")
    return redirect(f'https://frontend/auth/google?{params}')


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """retrieve user profile and update"""
    permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
