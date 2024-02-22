from rest_framework import generics, views, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating orders.

    Attributes:
    - queryset (QuerySet): The set of orders to be used in the view.
    - serializer_class (OrderSerializer): The serializer class to use for serializing orders.
    - http_method_names (list): The allowed HTTP methods for this view (POST and GET).
    - authentication_classes (list): The authentication classes used for authenticating requests.
    - permission_classes (list): The permission classes used for controlling access to the view.

    Methods:
    - post(request, *args, **kwargs): Handles POST requests to create a new order.

    Example:
    To create a new order, make a POST request with the required data to the endpoint.
    """

    serializer_class = OrderSerializer
    http_method_names = ["post", "get"]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        """
        Returns the queryset of orders for the authenticated user.
        """
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new order.

        Args:
        - request (Request): The HTTP request object.
        - *args (tuple): Additional arguments.
        - **kwargs (dict): Additional keyword arguments.

        Returns:
        - Response: The HTTP response containing the created order data or error messages.

        Example:
        To create a new order, make a POST request to the endpoint with the required data.
        """
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
