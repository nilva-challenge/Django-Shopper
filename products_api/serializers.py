from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Create serializer for product to convert data model into python json"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'count', 'price']
