import django_filters
from django.db.models import Q

from utils.drf_query_params_filter import RepeatedQueryParamFilter
from work.models.work import Work
from work.models.work_connection import WorkConnection


class WorkFilter(django_filters.FilterSet):
    without_rows = RepeatedQueryParamFilter(
        field_name='slug',
        param_name='without_rows',
        exclude=True,
    )

    without_types = RepeatedQueryParamFilter(
        field_name='type_id',
        param_name='without_types',
        exclude=True,
    )

    only_types = RepeatedQueryParamFilter(
        field_name='id',
        param_name='only_types',
    )

    only_statuses = RepeatedQueryParamFilter(
        field_name='status__status_id',
        param_name='only_statuses',
    )

    ids = RepeatedQueryParamFilter(
        field_name='id',
        param_name='ids',
    )

    execute_by_users = RepeatedQueryParamFilter(
        field_name='execute_by_id',
        param_name='execute_by_users',
    )

    type = django_filters.BaseInFilter(
        field_name='type',
        lookup_expr='in',
    )

    epic = RepeatedQueryParamFilter(
        field_name='epic__slug',
        param_name='epic',
    )

    sprint = django_filters.CharFilter(
        method='filter_by_sprint',
    )

    sprints = RepeatedQueryParamFilter(
        field_name='sprint__slug',
        param_name='sprints',
    )

    project = django_filters.CharFilter(
        method='filter_by_project',
    )

    created_by = django_filters.BaseInFilter(
        field_name='created_by',
        lookup_expr='in',
    )

    execute_by = django_filters.BaseInFilter(
        field_name='execute_by',
        lookup_expr='in',
    )

    without_sprints = django_filters.BooleanFilter(
        method='filter_without_sprints',
    )

    without_execute_by = django_filters.BooleanFilter(
        method='filter_without_execute_by',
    )

    class Meta:
        model = Work
        fields = []

    def filter_without_sprints(self, queryset, name, value):
        if value is True:
            return queryset.filter(sprint__isnull=True)
        return queryset

    def filter_without_execute_by(self, queryset, name, value):
        if value is True:
            return queryset.filter(execute_by__isnull=True)
        return queryset

    def filter_by_project(self, queryset, name, value):
        if value:
            return queryset.filter(project__slug=value)
        return queryset

    def filter_by_sprint(self, queryset, name, value):
        if value:
            return queryset.filter(sprint__slug=value)
        return queryset


class WorkConnectionFilter(django_filters.FilterSet):
    work = django_filters.CharFilter(method='filter_work')

    class Meta:
        model = WorkConnection
        fields = ['work', 'type']

    def filter_work(self, queryset, name, value):
        return queryset.filter(Q(work_from__slug=value) | Q(work_to__slug=value))
