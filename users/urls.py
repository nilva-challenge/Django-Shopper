from django.urls import path, include
from . import views

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    path('login/', views.UserAPIView.as_view(), name='login'),
    path('<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-detail'),
    # path('auth/', include('allauth.urls')),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/google/callback/', views.google_callback, name='google_callback'),
    path('auth/google/url/', views.google_views.oauth2_login),
]
