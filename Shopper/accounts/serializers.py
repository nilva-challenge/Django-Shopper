from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        # Checks if the user with the email exists
        try:
            user = User.objects.get(email=validated_data['email'])
            # Checks the password
            if not user.check_password(validated_data['password']):
                raise serializers.ValidationError('password is incorrect')
        except User.DoesNotExist:
            # Creates the User if the email doesnt exist in database
            user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'],
                                            password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']