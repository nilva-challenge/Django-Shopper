from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Create serializer for product to convert data model into python json"""

    class Meta:
        model = Product
        fields = ['id','name', 'count', 'price']


class OredrSerializer(serializers.ModelSerializer):
    """Create serializer for order to convert data model into python json"""

    class Meta:
        model = Order
        fields = ['user', 'product', 'count']
