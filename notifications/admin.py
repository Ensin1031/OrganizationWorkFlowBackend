from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user', 'is_read', 'is_active')
    list_display_links = ('id', 'created')
    list_filter = ('is_read', 'is_active')
    autocomplete_fields = ('user',)
    search_fields = ('id',)
    readonly_fields = ('slug', 'created', 'updated')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
