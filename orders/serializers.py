from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("order_date", "user", "id", )

    def validate(self, attrs):
        super(OrderSerializer, self).validate(attrs)

        product = attrs.get('product')
        count = attrs.get('count')
        if count > product.count:
            raise serializers.ValidationError(
                {
                    "count": {"detail": "This field is greater than given product.", "product_id": product.id, "product_title": product.title}
                }
            )
        return attrs
