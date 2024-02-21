from django.urls import path
from .views import *

urlpatterns = [
    path('email/', UserEmailLoginView.as_view(), name="email_login"),
    path('email/password/',
         UserPasswordLoginView.as_view(), name="password_login"),
    
    path('token/', CustomTokenObtainPairView.as_view(), name="token"),
]
