from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from products.serializers import ProductSerializer
from products.models import Product


class ProductListAPI(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.availables()
