from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer for login and signup"""
    class Meta:
        model = User
        fields = ['email', 'password']
        write_only = ['password']
        read_only = ['id']


class UserUpdateSerializer(serializers.ModelSerializer):
    """User serializer for see profiles and update"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth']
