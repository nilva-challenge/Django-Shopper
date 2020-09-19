from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListApiView.as_view()),
]
