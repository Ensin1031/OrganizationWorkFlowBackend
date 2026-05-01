from utils.model_mixins import UniqueNameMixin, ReferenceMixin


class WorkType(UniqueNameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работ'
