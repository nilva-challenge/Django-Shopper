from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.ProductListApiView.as_view(), name='products'),
    path('order/', views.OrderCreateViewSet.as_view(), name='order'),
]
