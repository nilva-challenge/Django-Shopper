from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        self.request_site = kwargs.pop('site', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save()
        return user

    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = UserChangeForm.Meta.fields


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'autocomplete': 'username',
        'autofocus': True,
    }))

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}), required=False)

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        'verify email': _("This account require email verification")
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the max length and label for the "email" field witch is username in model.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['email'].max_length = username_max_length
        self.fields['email'].widget.attrs['maxlength'] = username_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )