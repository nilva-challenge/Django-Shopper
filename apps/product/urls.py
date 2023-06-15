from django.urls import re_path, include
from rest_framework import routers

from apps.product.views import ListProduct

router = routers.SimpleRouter()
router.register("product",
                ListProduct,
                "/")

urlpatterns = [
    re_path("", include(router.urls))
]
