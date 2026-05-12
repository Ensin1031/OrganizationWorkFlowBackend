import django_filters

from comments.models import WorkComment


class WorkCommentFilter(django_filters.FilterSet):

    work = django_filters.CharFilter(
        field_name='work__slug',
        lookup_expr='exact',
    )

    parent = django_filters.CharFilter(
        field_name='parent__slug',
        lookup_expr='exact',
    )

    created_by = django_filters.NumberFilter(
        field_name='created_by__id',
        lookup_expr='exact',
    )

    class Meta:
        model = WorkComment
        fields = ['created_by', 'work', 'parent']
