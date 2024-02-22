from django.urls import path
from .views import UserProfileView, UserEmailLoginView, UserPasswordLoginView, GitHubLogin

urlpatterns = [
    path('login/', UserEmailLoginView.as_view(), name="email_login"),
    path('login/password/',
         UserPasswordLoginView.as_view(), name="password_login"),

    path('github/login/',
         GitHubLogin.as_view(), name="github_login"),

    path('profile/',
         UserProfileView.as_view(), name="profile"),
]
