from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='products_list'),
    path('order/', OrderListCreateView.as_view(), name='order'),
]
