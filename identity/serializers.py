from rest_framework import serializers

from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

# Authentication Serializers


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


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user profile.

    Attributes:
    - model (User): The User model class.
    - fields (list): The fields to include in the serialized output.

    Example:
    To serialize user profile data, create an instance of this serializer with a User instance.
    The serialized data will include 'first_name', 'last_name', 'email', and 'username' fields.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
