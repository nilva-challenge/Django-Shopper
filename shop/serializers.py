from rest_framework import serializers, exceptions
from .models import Product, Order, OrderItem

from django.utils.translation import gettext_lazy as _


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        product_id = attrs.get('product')

        if product_id:
            try:
                product = Product.objects.get(name=product_id)
            except Product.DoesNotExist:
                msg = _('Product with this number does not exist.')
                raise exceptions.ValidationError(msg)

            if quantity > product.in_stock:
                msg = _('This number of products does not exist.')
                raise exceptions.ValidationError(msg)

        return attrs
