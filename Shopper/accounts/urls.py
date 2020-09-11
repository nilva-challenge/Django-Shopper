from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='accounts-create'),

]