from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from orders.serializers import OrderSerializer


class OrdersAPI(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        """
        This endpoint is for submitting orders. In the body you can send one object or list of objects.
        each object includes product id and count of the order:
        {
            product: <int>,
            count: <int>
        }

        Returns:
            if order is valid then you will recieve a complete object of that order:
                {
                    "id": 5,
                    "count": 2,
                    "order_date": "2020-09-16",
                    "user": 1,
                    "product": 1
                }
            if order is not valid you will recieve realted error details:
                404 example with 2 objects:
                    [
                        {},
                        {
                            "product": [
                                "Invalid pk \"43\" - object does not exist."
                            ]
                        }
                    ]
                400 example with 2 objects:
                    [
                        {
                            "count": {
                                "detail": "This field is greater than given product.",
                                "product_id": "1",
                                "product_title": "Apple"
                            }
                        },
                        {
                            "count": {
                                "detail": "This field is greater than given product.",
                                "product_id": "3",
                                "product_title": "Banana"
                            }
                        }
                    ]

        """
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        """
        Simple List endpoint for orders
        """
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(data=serializer.data)
