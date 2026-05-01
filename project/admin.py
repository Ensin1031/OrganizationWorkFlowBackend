from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline

from project.models import Project, ProjectStatus, ProjectVersion
from utils.model_admin_mixins import ReferencesAdminMixin


class ProjectStatusNestedInLine(NestedTabularInline):

    model = ProjectStatus
    autocomplete_fields = ('project', 'status',)
    extra = 0


class ProjectVersionNestedInLine(NestedTabularInline):

    model = ProjectVersion
    autocomplete_fields = ('project',)
    readonly_fields = ('slug', )
    extra = 0


@admin.register(Project)
class ProjectAdmin(ReferencesAdminMixin, NestedModelAdmin):
    list_display = ('id', 'code_prefix', 'name', 'slug', 'is_active')
    list_display_links = ('id', 'code_prefix', 'name', 'slug')
    inlines = (ProjectStatusNestedInLine, ProjectVersionNestedInLine)
    readonly_fields = ('slug', 'created', 'updated')


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'status', 'is_active')
    list_filter = ('is_active',)
    autocomplete_fields = ('project', 'status')
    search_fields = ('id',)


@admin.register(ProjectVersion)
class ProjectVersionAdmin(ReferencesAdminMixin):
    list_display = ('id', 'name', 'project', 'is_active')
    list_display_links = ('id', 'name',)
    list_filter = ('is_active',)
    autocomplete_fields = ('project',)
    readonly_fields = ('slug', 'created', 'updated')
