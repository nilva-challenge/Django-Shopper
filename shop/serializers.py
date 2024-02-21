from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Attributes:
    - model:class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available_quantity']

    Note: Make sure to replace 'Product' with the actual model class name if it differs.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available_quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity',)
        read_only_fields = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'order_date', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else User.objects.first()
        order = Order.objects.create(
            user=user,)

        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            try:
                Product.objects.get(id=product.id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    {"product_id": f"Product with ID {product} does not exist."})

            OrderItem.objects.create(
                order=order, product=product, quantity=quantity)

        return order


{
    "user": 1,
    "order_items": [
        {
            "product":
                1,
            "quantity": 5
        },
        {
            "product":
                2,
            "quantity": 2
        },
        {
            "product":
                3,
            "quantity": 4
        }
    ]
}
