from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [

    path('admin/', admin.site.urls),

    path('shop/', include('shopper.urls')),
    path('user-panel/', include('user_panel.urls')),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
