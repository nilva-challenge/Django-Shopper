from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    # Custom Redirecting
    def get_logout_redirect_url(self, request):
        path = "/accounts/login/"
        return path
