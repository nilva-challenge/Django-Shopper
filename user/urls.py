from django.urls import path
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView

from user.views import CustomLoginView, SignUpView, PostLogoutView, CustomPasswordChangeView

app_name = 'user'

urlpatterns = [
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    path('signup/', SignUpView.as_view(), name='signup'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', PostLogoutView.as_view(), name='logout'),
    path('logout/done/',
         TemplateView.as_view(template_name='registration/logged_out.html'), name='logout_done'),

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_view.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_view.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
