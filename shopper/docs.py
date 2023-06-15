from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication

from shopper import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Shopper Test Project",
        default_version="0.1.0",
        description="swagger for check apis",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email='test@test.com',
                                license=openapi.License(name="MIT License"), ),
        public=True,
        authentication_classes=[SessionAuthentication],
    ))

# noinspection PyUnresolvedReferences
urlpatterns = [
    re_path(r'', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
