from typing import Union, List, Tuple

from django.contrib import admin


def add_admin_fields(fields: Union[List, Tuple], fields_list: Union[List, Tuple]):
    output_fields = fields
    for field_name in fields_list:
        if not output_fields:
            output_fields = tuple((field_name,))
        else:
            if field_name not in list(fields):
                output_fields = output_fields + (field_name,)
    return output_fields


class ReferencesAdminMixin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    list_display_links = ('id', 'name', 'slug')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('slug', 'created', 'updated')
