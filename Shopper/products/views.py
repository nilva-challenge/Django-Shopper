from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import product, OrderItem, Order
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def ProductsList(request):
    """
    Returns available products
    """
    if request.method == 'GET':
        # Retrieve available and not sold products
        available_products = product.objects.filter(quantity__gt=0, is_available=True)
        serializer = ProductSerializer(available_products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def order(request):
    """
    Records the order in data with
    list of product ids and their quantity.
    returns 400 status if quantity or product id is invalid.
    """
    if request.method == 'POST':
        order_items = request.data
        # Checks if any of products id or quantity is invalid
        for item in order_items:
            try:
                item_product = product.objects.get(pk=item['product'])
            except product.DoesNotExist:
                return Response("product id is incorrect.", status=status.HTTP_400_BAD_REQUEST)
            quantity = item['quantity']
            if quantity > item_product.quantity:
                return Response("not enough product.", status=status.HTTP_400_BAD_REQUEST)

        # Creates new order for order items
        order = Order(costumer=request.user)
        order.save()
        # Creates order item objects and set the order of them to new order declared above
        for item in order_items:
            item_product = product.objects.get(pk=item['product'])
            quantity = item['quantity']
            item_product.quantity -= quantity
            item_product.save()
            OrderItem.objects.create(quantity=quantity, order=order, product=item_product)
            
        return Response(status=status.HTTP_201_CREATED)
