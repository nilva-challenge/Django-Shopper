from django.contrib import admin
from django.urls import path, include
# from allauth.account.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('profiles_api.urls')),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products_api.urls')),
    path('', include('pages.urls')),
]
