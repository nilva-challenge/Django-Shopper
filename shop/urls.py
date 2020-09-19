from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shopper.urls')),
    path('user-panel/', include('user_panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
