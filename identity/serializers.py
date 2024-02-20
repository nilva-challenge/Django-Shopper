from rest_framework import serializers

from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
from typing import Any, Dict

from .custom_classes import CacheManager

User = get_user_model()

# Authentication Serializers


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def validate(self, attrs: Dict[str, Any]):
        data = super().validate(attrs)

        access = self.get_token(self.user)

        data["access"] = str(access)

        return data

    def create(self, validated_data):
        """
        Creates a new user instance with the provided data.

        Args:
            validated_data (dict): The validated data containing user information.

        Returns:
            User: The newly created user instance.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        password = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserEmailLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate the email address using the EmailValidator.
        """
        validator = EmailValidator("Enter a valid email address.")
        validator(value)
        return value


class UserPasswordLoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True, label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        password = attrs.get('password')

        try:
            validate_password(password, self.instance)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs


