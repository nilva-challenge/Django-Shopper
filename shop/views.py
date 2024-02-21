from rest_framework import generics, views, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .serializers import *

User = get_user_model()


class ProductListCreateView(generics.ListCreateAPIView):
    """
    View to create one and retrieve all products that are not sold.

    Authentication is required to access this view.
    """
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset for retrieving non-sold products.

        Returns:
        - QuerySet: QuerySet of products that are not sold.
        """
        return [product for product in Product.objects.all() if not product.is_sold]


# class OrderView(generics.ListCreateAPIView):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # http_method_names = ["post", "get"]
    # # authentication_classes = [TokenAuthentication]
    # permission_classes = [AllowAny]


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["post", "get"]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
