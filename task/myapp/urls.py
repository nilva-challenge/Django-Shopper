from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from myapp.views import ApiLogin,ApiProfile,ApiProduct,ApiOrder,SocialToken
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('login/',ApiLogin,name="login"),
    path('profile/', ApiProfile, name="profile"),
    path('product/', ApiProduct, name="product"),
    path('order/', ApiOrder, name="order"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('social_token/', SocialToken, name='social_token'),
    path('accounts/', include('allauth.urls')),
]