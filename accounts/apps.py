from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        """
        Connects signals when app is in ready state
        """
        from accounts import signals
