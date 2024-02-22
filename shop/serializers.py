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
    """
    Serializer for the OrderItem model.

    Attributes:
    - product (int): The ID of the associated product.
    - quantity (int): The quantity of the product in the order.

    Meta:
    - model (OrderItem): The OrderItem model class.
    - fields (tuple): The fields to include in the serialized output.
    - read_only_fields (tuple): The fields that are read-only and not to be modified.

    Example:
    serializer = OrderItemSerializer(data={'product': 1, 'quantity': 2})
    if serializer.is_valid():
        order_item_instance = serializer.save()
    """
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity',)
        read_only_fields = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Attributes:
    - order_date (datetime): The date and time of the order.
    - order_items (list): List of OrderItemSerializer instances representing the items in the order.

    Methods:
    - create(validated_data): Creates a new order with the specified order items.

    Example:
    serializer = OrderSerializer(data={'order_items': [{'product': 1, 'quantity': 2}]})
    if serializer.is_valid():
        order_instance = serializer.save()
    """
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_date', 'order_items']

    def create(self, validated_data):
        """
        Creates a new order with the specified order items.

        Args:
        - validated_data (dict): Validated data containing order details and items.

        Returns:
        - Order: The created order instance.

        Raises:
        - serializers.ValidationError: If there are issues with product existence or insufficient quantity.

        Example Data:
        {
            "order_items":
            [
                {
                "product":1,
                "quantity": 1
                },
                {
                "product":2,
                "quantity": 4
                },
            ]
        }
        """
        order_items_data = validated_data.pop('order_items', [])
        request = self.context.get('request')
        user = request.user
        order = Order.objects.create(user=user)

        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            try:
                product_instance = Product.objects.get(id=product.id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    {"product_id": f"Product with ID {product} does not exist."})

            if quantity > product_instance.available_quantity:
                raise serializers.ValidationError(
                    {"quantity": f"Insufficient quantity for product  {product}"})

            OrderItem.objects.create(
                order=order, product=product, quantity=quantity)

            product_instance.available_quantity -= quantity
            product_instance.save()

        return order
