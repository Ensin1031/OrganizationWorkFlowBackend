import django_filters


class RepeatedQueryParamFilter(django_filters.Filter):
    def __init__(self, *args, param_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.param_name = param_name or self.field_name

    def filter(self, qs, value):
        values = self.parent.request.query_params.getlist(self.param_name)

        if not values:
            return qs

        lookup = f'{self.field_name}__in'

        if self.exclude:
            return qs.exclude(**{lookup: values})

        return qs.filter(**{lookup: values})
