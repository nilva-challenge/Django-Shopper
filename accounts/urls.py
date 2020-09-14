from django.urls import path

from accounts.api import LoginAPI

api_namespace = 'api/v1/accounts/'
urlpatterns = [
    path(api_namespace + 'login/', LoginAPI.as_view(), name='login_api')
]
