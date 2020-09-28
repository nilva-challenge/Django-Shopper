from django.contrib import admin
from .models import SocialProvider, SocialAccount

admin.site.register(SocialProvider)
admin.site.register(SocialAccount)
