from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()

# Authentication Serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available_quantity']
