from django.urls import path

from products.api import ProductListAPI

api_namespace = 'api/v1/products/'
urlpatterns = [
    path(api_namespace, ProductListAPI.as_view(), name='products_api')
]
