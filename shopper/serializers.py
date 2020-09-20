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


class OrderingSerializer(serializers.Serializer):
    """Serializer for ordering"""
    pass


class ProductOrderSerializer(serializers.ModelSerializer):
    """Serializers for product"""

    class Meta:
        model = models.Product
        fields = (
            'id',
            'name',
            'price'
        )


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order item"""
    product = ProductOrderSerializer(many=False)

    class Meta:
        model = models.OrderItem
        exclude = ['order']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'name'
        )


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order model"""
    user = UserSerializer(many=False)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = '__all__'
