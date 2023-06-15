from django.urls import re_path, include
from rest_framework import routers

from apps.user.views import UserLogin

router = routers.SimpleRouter()
router.register("login",
                UserLogin,
                "/")

urlpatterns = [
    re_path("", include(router.urls))
]
