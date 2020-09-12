from django.shortcuts import render
from rest_framework import authentication, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import product, OrderItem, Order
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def ProductsList(request):
    if request.method == 'GET':
        available_products = product.objects.filter(quantity__gt=0, is_available=True)
        serializer = ProductSerializer(available_products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def order(request):
    if request.method == 'POST':
        order_items = request.data

        for item in order_items:
            try:
                item_product = product.objects.get(pk=item['product'])
            except product.DoesNotExist:
                return Response("product id is incorrect.", status=status.HTTP_400_BAD_REQUEST)
            quantity = item['quantity']
            if quantity > item_product.quantity:
                return Response("not enough product.", status=status.HTTP_400_BAD_REQUEST)

        for item in order_items:
            order = Order(costumer=request.user)
            order.save()
            item_product = product.objects.get(pk=item['product'])
            item_product.quantity -= quantity
            item_product.save()
            OrderItem.objects.create(quantity=quantity, order=order, product=item_product)
            
        return Response(status=status.HTTP_201_CREATED)
