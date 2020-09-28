from django.urls import path
from user_api import views

app_name = 'user-api'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('retrieve-update-deactivate/', views.RetrieveUpdateDestroyUserView.as_view(),
         name='retrieve-update-deactivate'),
    path('deactivate/', views.DeactivateUserView.as_view(), name='deactivate'),

    path('token/', views.CreateTokenView.as_view(), name='token'),

    # path('auth/google/', social_views.GoogleLogin.as_view(), name='google_login'),
    # path('auth/google/url/', google_views.oauth2_login)

    # path('direct/create_login/', create_login , name='create_login')
]
# user-api:create
