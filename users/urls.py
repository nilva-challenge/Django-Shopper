from django.urls import path, include
from . import views

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    path('login/', views.UserAPIView.as_view(), name='login'),
    path('<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-detail'),
]
