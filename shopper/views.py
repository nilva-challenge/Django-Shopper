from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from core import models
from . import serializers


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
        """
            Function that adding quantity to existing product in order
        """
        for product in products:
            if product['id'] == key:
                product['quantity'] += value

    def create(self, request, *args, **kwargs):
        data_items = request.data
        products = []

        # check product id is available and check quantity must be more than 0
        for product in data_items:
            # this error handler is for not existing product
            try:
                # try to get object by id
                temp = models.Product.objects.get(id=product['id'])

                # check product is available
                if temp.stock == 0:
                    res = {
                        'message': 'The order contains unavailable products!'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                # check quantity that user want is positive
                if product['quantity'] <= 0:
                    res = {
                        'message': f'The quantity of {temp.name} is lower than one!'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

            except models.Product.DoesNotExist:
                res = {
                        'message': 'The product not found!'
                    }
                return Response(res, status=status.HTTP_404_NOT_FOUND)

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
        price = 0  # for total price
        # create new order
        order = models.Order.objects.create(user=request.user, price=price)

        # this is for compute total price and add order item to database
        for product in products:
            product_obj = models.Product.objects.get(id=product['id'])
            price += product_obj.price * product['quantity']
            models.OrderItem.objects.create(
                order=order,
                product_id=product['id'],
                quantity=product['quantity']
            )
            product_obj.stock -= product['quantity']  # minus product stock from quantity of this order
            product_obj.save()
        # save total price
        order.price = price
        order.save()

        res = {
            'message': 'Your order has been successfully registered',
            'data': serializers.OrderSerializer(order).data
        }

        return Response(
            res,
            status=status.HTTP_201_CREATED
        )
