from django.contrib import admin

from sprint.models import Sprint
from utils.model_admin_mixins import ReferencesAdminMixin


@admin.register(Sprint)
class SprintAdmin(ReferencesAdminMixin):
    list_display = ('id', 'name', 'slug', 'start_date', 'end_date', 'in_work', 'is_completed', 'is_active')
    list_display_links = ('id', 'name', 'slug')
    list_filter = ('in_work', 'is_completed', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('slug', 'created', 'updated')
