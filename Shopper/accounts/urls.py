from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # Regular Authentication with Token
    path('login/', views.UserAPI.as_view(), name='accounts-create'),
    # API for editing and observing the authenticated user
    path('profile/', views.UserProfile.as_view() , name='profile')
]
