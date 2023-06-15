from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from apps.user.exceptions import UnAuthorizedUser
from apps.user.models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise UnAuthorizedUser
        except User.DoesNotExist as e:
            print(e)
            user = User()
            user.email = email
            user.password = user.set_password(password)
            user.save()
        self.token, _ = Token.objects.get_or_create(user=user)
        return self
