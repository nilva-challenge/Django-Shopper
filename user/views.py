from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import views
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from user.forms import CustomUserCreationForm, CustomAuthenticationForm
from user.models import EmailUser


@method_decorator(require_http_methods(["POST", ]), name='dispatch')
class PostLogoutView(views.LogoutView):
    """only with Post request user can log out,
    this add up to security."""
    next_page = reverse_lazy('user:logout_done')

    # @method_decorator(require_http_methods(["POST", ]))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    # todo: make a active your email account template
    success_url = reverse_lazy('user:login')
    template_name = 'registration/signup.html'

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view.
        modified to pass request object to form instance"""
        if form_class is None:
            form_class = self.get_form_class()

        kwargs = self.get_form_kwargs()
        from django.contrib.sites.shortcuts import get_current_site
        kwargs['site'] = get_current_site(self.request)

        return form_class(**kwargs)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    extra_context = {'next': reverse_lazy('user:index')}


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch', )
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('user:password_change_done')


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch', )
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_email_verified)
        )


account_activation_token = TokenGenerator()