from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginUserAPI),
    path('products/', views.ProductList.as_view()),
    path('profile/', views.Profile.as_view()),
    path('order/', views.OrderList.as_view()),
]