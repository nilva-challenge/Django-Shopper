# identity/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']


# Register the custom user model with the admin site
admin.site.register(User, CustomUserAdmin)
