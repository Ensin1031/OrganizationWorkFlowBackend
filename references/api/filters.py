import django_filters

from references.models.work_type import WorkType
from utils.drf_query_params_filter import RepeatedQueryParamFilter


class WorkTypeFilter(django_filters.FilterSet):
    without = RepeatedQueryParamFilter(
        field_name='id',
        param_name='without',
        exclude=True,
    )

    only = RepeatedQueryParamFilter(
        field_name='id',
        param_name='only',
    )

    class Meta:
        model = WorkType
        fields = []
