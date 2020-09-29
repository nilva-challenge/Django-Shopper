

from . import views
from django.urls import path, include


urlpatterns = [
   # url(r'^check$', views.check_token, name='check token'),
   # url(r'^login$', views.v1login, name='login'),
   path('login_with_email', views.login_with_email, name='login_with_email'),
   path('sign_in_with_google', views.sign_in_with_google, name='sign_in_with_google'),
   path('get_my_profile', views.get_my_profile, name='get_my_profile'),
   path('update_my_profile', views.update_my_profile, name='update_my_profile'),
   # url(r'^register$', views.register, name='register for first time'),
]
