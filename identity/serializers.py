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
    """
    Custom token obtain pair serializer.

    Attributes:
    - token_class: The token class used for authentication (AccessToken).

    Methods:
    - validate(attrs: Dict[str, Any]) -> Dict[str, Any]:
        Validate the provided attributes and generate an access token.

    - create(validated_data: Dict[str, Any]) -> User:
        Create a new user instance with the provided data.

        Args:
        - validated_data (dict): The validated data containing user information.

        Returns:
        - User: The newly created user instance.

        Raises:
        - serializers.ValidationError: If the passwords do not match.
    """

    token_class = AccessToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the provided attributes and generate an access token.

        Args:
        - attrs (dict): The attributes to be validated.

        Returns:
        - dict: The validated data with the access token.

        Raises:
        - serializers.ValidationError: If validation fails.
        """
        data = super().validate(attrs)
        access = self.get_token(self.user)
        data["access"] = str(access)
        return data

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Create a new user instance with the provided data.

        Args:
        - validated_data (dict): The validated data containing user information.

        Returns:
        - User: The newly created user instance.

        Raises:
        - serializers.ValidationError: If the passwords do not match.
        """
        password = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserEmailLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login with email.

    Fields:
    - email: EmailField representing the user's email address.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate the email address using the EmailValidator.

        Parameters:
        - value (str): The email address to be validated.

        Returns:
        str: The validated email address.

        Raises:
        serializers.ValidationError: If the email address is not valid.
        """
        validator = EmailValidator("Enter a valid email address.")
        validator(value)
        return value


class UserPasswordLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login with password.

    Fields:
    - password: CharField representing the user's password (write-only).
    """

    password = serializers.CharField(
        write_only=True, label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        """
        Validate the password using Django's validate_password function.

        Parameters:
        - attrs (dict): Dictionary containing the password to be validated.

        Returns:
        dict: The validated attributes.

        Raises:
        serializers.ValidationError: If the password is not valid.
        """
        password = attrs.get('password')

        try:
            validate_password(password, self.instance)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
