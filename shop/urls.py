from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products_list'),
]
