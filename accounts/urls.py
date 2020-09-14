from django.urls import path

from accounts.api import LoginAPI, GoogleLoginAPI
from accounts.views import GoogleAuthView

api_namespace = 'api/v1/accounts/'
urlpatterns = [
    path(api_namespace + 'login/', LoginAPI.as_view(), name='login_api'),
    path(api_namespace + 'login/google/', GoogleLoginAPI.as_view(), name='google_login_api'),
    path('accounts/google/auth/', GoogleAuthView.as_view(), name='google_auth_page'),
]
