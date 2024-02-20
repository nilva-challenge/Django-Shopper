from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *

User = get_user_model()

# Authentication Views


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserEmailLoginView(generics.CreateAPIView):
    serializer_class = UserEmailLoginSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', '')

        redirect_url = reverse('password_login') + \
            f'?email={email}'

        return HttpResponseRedirect(redirect_url, email, )


class UserPasswordLoginView(generics.CreateAPIView):
    serializer_class = UserPasswordLoginSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', '')

        return Response({'email': email})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = self.request.query_params.get('email', '')
        password = serializer.validated_data['password']

        try:

            user = User.objects.get(email=email)

            if not check_password(password, user.password):
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            try:
                user = User.objects.create_user(username=email,email=email, password=password)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = CacheManager.set_cache_token(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
