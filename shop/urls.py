from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet, basename='Order')
router.register('order-items', views.OrderItemViewSet)

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls)),
]
