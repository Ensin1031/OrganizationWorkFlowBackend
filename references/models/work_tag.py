from utils.model_mixins import UniqueNameMixin, ReferenceMixin


class WorkTag(UniqueNameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Тэг работы'
        verbose_name_plural = 'Тэги работ'
