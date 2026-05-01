from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import UserExtended


@admin.register(UserExtended)
class UserExtendedAdmin(UserAdmin):
    pass
