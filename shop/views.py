from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import *

User = get_user_model()

class ProductListView(generics.ListAPIView):
    """
    View to retrieve all products that are not sold.

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
        return Product.objects.filter(is_sold=False)