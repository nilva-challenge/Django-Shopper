from django.urls import path

from orders.api import OrdersAPI

api_namespace = "api/v1/orders/"
urlpatterns = [
    path(api_namespace, OrdersAPI.as_view(), name="orders_api"),
]
