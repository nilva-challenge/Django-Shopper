from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models

class ProductSerializer(serializers.ModelSerializer):
    """Serializers for product"""

    class Meta:
        model = models.Product
        fields = (
            'id',
            'name',
            'stock',
            'price'
        )
