from django.contrib import admin

from work.models.work import Work
from work.models.work_connection import WorkConnection


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    list_display_links = ('id', 'name', 'slug',)
    search_fields = ['name', 'slug']
    autocomplete_fields = (
        'epic', 'histories', 'type', 'priority', 'project', 'sprint', 'status',
        'created_by', 'execute_by', 'difficulty', 'technology',
    )
    filter_horizontal = ('tags', 'versions')
    readonly_fields = ('created', 'updated', 'slug')


@admin.register(WorkConnection)
class WorkConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'work_from', 'work_to')
    list_display_links = ('id', 'type',)
    search_fields = ['id']
    autocomplete_fields = ('work_from', 'work_to')
