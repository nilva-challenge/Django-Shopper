from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.UserAPI.as_view(), name='accounts-create'),
    path('profile/', views.UserProfile.as_view())
]