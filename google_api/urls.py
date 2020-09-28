from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # caller (calls google api) and assign the redirect url from the google by the google_caller_url_name argument
    # argument: google_caller_url_name is the name of the url will be resolved and send as redirect url to google API
    path('google/api_caller/<str:google_caller_url_name>/', views.google_call, name='google_call'),
    # call backs from google api (use these url names in <str:google_caller_url_name> in the upper)
    path('google/callback/signup/', views.google_callback_signup, name='google_callback_signup'),
    path('google/callback/login/', views.google_callback_login, name='google_callback_login'),
    path('google/callback/login_signup/', views.google_callback_login_signup, name='google_callback_login_signup'),
    path('google/callback/add_social/', views.google_callback_add_social, name='google_callback_add_social'),
    path('google/callback/revoke/', views.google_callback_revoke, name='google_callback_revoke'),
    # end of call backs

    # google_ajax_url_name: is the name of url which wbe will called by ajax client json post request
    path('google/ajax_caller/<str:google_ajax_url_name>/', views.TemplateCSRFView.as_view(), name='google_ajax'),
    # call from js api through ajax POST json
    path('google/ajax_post/signup/', views.GoogleSignupAjaxView.as_view(), name='google_ajax_signup'),
    path('google/ajax_post/login/', views.GoogleAjaxLoginView.as_view(), name='google_ajax_login'),
    path('google/ajax_post/add_social/', views.GoogleAjaxAddSocialView.as_view(), name='google_ajax_add_social'),


    path('google/ajax/login_signup_add_social/', views.GoogleLoginSignupConnectAjaxView.as_view(),
         name='google_ajax_add_social_login_connect'),
    # end of ajax POST JSON

    # REST API
    path('google/REST/login_signup_add_social/', views.GoogleLoginSignupConnectRESTView.as_view(),
         name='google_rest_add_social_login_connect'),

    # template example
    path('google/oauth/', TemplateView.as_view(template_name='google_api/google_python.html'), name='google'),
    path('google/javascript/', TemplateView.as_view(template_name='google_api/google_api.html'), name='google'),

    path('google/error/', TemplateView.as_view(template_name='google_api/google_python.html', ),
         name='google_error'),
]
