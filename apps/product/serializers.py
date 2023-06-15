from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):


        return