from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.serializers import LoginSerializer
from accounts.utils import get_user, User


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
