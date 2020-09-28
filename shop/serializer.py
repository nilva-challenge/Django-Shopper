from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from django.db import transaction

from .models import Items, Orders


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        item = Items.objects.get(id=validated_data['item'].id)
        amount = validated_data['amount']
        if item.amount >= amount:
            item.amount -= amount
        else:
            raise ValidationError(detail='order amount is more than available amount', code='not_enough_amount')

        order = Orders.objects.create(**validated_data)
        item.save()

        return order
