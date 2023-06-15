from rest_framework import viewsets
from rest_framework.response import Response

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.user.permissions import IsSellerUser, IsAdminUser, IsCustomerUser


class ListProduct(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get']
    permission_classes = [IsAdminUser | IsSellerUser | IsCustomerUser]

    # queryset = Product.objects.all()

    #
    def get_queryset(self):
        if IsSellerUser().has_permission(request=self.request, view=self) or IsAdminUser().has_permission(
                request=self.request, view=self):
            queryset = Product.objects.all()
        elif IsCustomerUser().has_permission(request=self.request, view=self):
            queryset = Product.objects.filter(is_exists=True)
        else:
            queryset = None
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    class RetrieveModelMixin:
        """
        Retrieve a model instance.
        """

        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
