from utils.model_mixins import UniqueNameMixin, ReferenceMixin


class WorkPriority(UniqueNameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Приоритет работы'
        verbose_name_plural = 'Приоритеты работ'
