from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('profiles_api.urls')),
    path('products/', include('products_api.urls')),
]
