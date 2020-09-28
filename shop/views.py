from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializer import ItemSerializer, OrdersSerializer
from .models import Items, Orders


class ItemListView(ListAPIView):
    """
    list item available to sell
    """
    queryset = Items.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ItemSerializer


class OrderListCreateView(ListCreateAPIView):
    """
    order items,
    see orders
    """
    queryset = Orders.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = OrdersSerializer
