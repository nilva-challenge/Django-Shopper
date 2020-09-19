from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from . import serializers
import requests
from core import models
import json
from django.shortcuts import get_object_or_404


class ProductListApiView(generics.ListAPIView):
    """
        API endpoint for listing available products
    """
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = models.Product.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(stock__gt=0)
        return queryset


class OrderCreateViewSet(generics.CreateAPIView):
    """
        API endpoint for order products
    """
    serializer_class = serializers.OrderingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @staticmethod
    def sum_quantity_by_id(key, value, products):
        for product in products:
            if product['id'] == key:
                product['quantity'] += value

    def create(self, request, *args, **kwargs):
        data = request.data
        print(request.data)
        data_items = data['products']
        products = []

        print(json.loads(data_items))

        # check product id is available and check quantity must be more than 0
        for product in data_items:
            try:
                temp = models.Product.objects.get(id=product['id'])
                if temp.stock == 0:
                    res = {
                        'message': 'The order contains unavailable products!'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                if product['quantity'] <= 0:
                    res = {
                        'message': f'The quantity of {temp.name} is lower than one!'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            except models.Product.DoesNotExist:
                res = {
                        'message': 'The order contains unavailable products!'
                    }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # sum quantity of same product
        for product in data_items:
            if product['id'] not in [item['id'] for item in products]:
                temp = {
                    'id': product['id'],
                    'quantity': product['quantity']
                }
                products.append(temp)
            else:
                self.sum_quantity_by_id(product['id'], product['quantity'], products)

        # check quantity of products isn't more than our inventory
        for product in products:
            product_obj = models.Product.objects.get(id=product['id'])
            if product['quantity'] > product_obj.stock:
                res = {
                    'message': f'The quantity of {product_obj.name} is more than our inventory!'
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # save product item in database
        price = 0
        order = models.Order.objects.create(user=request.user, price=price)
        for product in products:
            product_obj = models.Product.objects.get(id=product['id'])
            price += product_obj.price * product['quantity']
            models.OrderItem.objects.create(
                order=order,
                product_id=product['id'],
                quantity=product['quantity']
            )
            product_obj.stock -= product['quantity']
            product_obj.save()
        order.price = price
        order.save()
        print(serializers.OrderSerializer(order))
        res = {
            'message': 'Your order has been successfully registered',
            'data': serializers.OrderSerializer(order).data
        }
        return Response(
            res,
            status=status.HTTP_201_CREATED
        )


