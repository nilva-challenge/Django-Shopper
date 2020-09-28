from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('extended'), {'fields': ('site', 'is_email_verified',)}),
        (_('Username'), {'fields': ('username',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'username', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name', 'username',)
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)
