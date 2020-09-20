from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/token/', views.google_login_token, name='google-token'),
    path('me/', views.UserRetrieveUpdateApiView.as_view(), name='me')
]
