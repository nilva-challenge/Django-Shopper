from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
            if not user.check_password(validated_data['password']):
                raise serializers.ValidationError('password is incorrect')
        except User.DoesNotExist:
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