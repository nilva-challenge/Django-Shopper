from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('products_list/', views.ProductsList, name='products-list'),
    path('order/', views.order, name='order')
]