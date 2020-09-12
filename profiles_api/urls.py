from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
app_name = 'profiles_api'

router = DefaultRouter()
router.register('profile',views.UserProfileViewSet)

urlpatterns =[
    path('auth_token/', views.authenticate_user,name='login_user'),
    path('',include(router.urls)),
]