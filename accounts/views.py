from django.views.generic import TemplateView

class GoogleAuthView(TemplateView):
    template_name = 'accounts/google_auth.html'
