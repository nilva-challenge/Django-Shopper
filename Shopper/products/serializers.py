from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['name', 'quantity']



