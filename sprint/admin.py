from django.contrib import admin

from sprint.models import Sprint
from utils.model_admin_mixins import ReferencesAdminMixin


@admin.register(Sprint)
class SprintAdmin(ReferencesAdminMixin):
    list_display = ('id', 'name', 'slug', 'start_date', 'end_date', 'is_active')
    list_display_links = ('id', 'name', 'slug')
    readonly_fields = ('slug', 'created', 'updated')
