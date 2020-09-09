from rest_framework.viewsets import ModelViewSet
from .models import Product,Order
from .serializers import ProductSerializer
from . import permissions

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.AdminUpdateProduct,)

