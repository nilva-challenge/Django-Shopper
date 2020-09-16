from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from myapp.views import ApiLogin,ApiProfile,ApiProduct,ApiOrder

urlpatterns = [
    path('login/',ApiLogin,name="login"),
    path('profile/', ApiProfile, name="profile"),
    path('product/', ApiProduct, name="product"),
    path('order/', ApiOrder, name="order"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]