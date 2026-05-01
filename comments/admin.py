from django.contrib import admin

from comments.models import WorkComment


@admin.register(WorkComment)
class WorkCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'work', 'is_active')
    list_filter = ('is_active',)
    autocomplete_fields = ('created_by', 'work', 'parent')
    search_fields = ('id',)
    readonly_fields = ('slug', 'created', 'updated')
