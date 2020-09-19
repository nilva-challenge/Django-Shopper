from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from . import serializers
import requests
from core import models


class ProductListApiView(generics.ListAPIView):
    """
        API endpoint for listing available products
    """
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(stock__gt=0)
        return queryset
