from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.user.exceptions import UnAuthorizedUser
from apps.user.models import User
from apps.user.serializers import UserSerializer


class UserLogin(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except UnAuthorizedUser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
