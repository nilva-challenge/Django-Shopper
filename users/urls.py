from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserAPIView.as_view(), name='login'),
    path('<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-detail'),
]
