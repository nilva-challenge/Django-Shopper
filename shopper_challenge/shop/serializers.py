from rest_framework import serializers

from .models import Product, Order, CustomUser


# Products Model Seriazlizer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' ,'productTitle', 'stock']


# Orders Model Seriazlizer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity']
        

# User Model Seriazlizer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id' ,'email']