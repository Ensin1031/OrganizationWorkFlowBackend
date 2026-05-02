from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import UserExtended


@admin.register(UserExtended)
class UserExtendedAdmin(UserAdmin):
    readonly_fields = ('date_joined', 'last_login', 'created', 'updated', 'slug')
    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'slug',
        )}),
        (_('Personal info'), {
            'fields': (
                'email', 'first_name', 'second_name', 'last_name', 'is_verified',
            )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active', 'is_superuser', 'groups', 'user_permissions',
                ),
                'classes': ('collapse',),
            }),
        (_('Important dates'), {
            'fields': (
                'last_login', 'date_joined', 'created', 'updated',
            ),
            'classes': ('collapse',),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email')
