from utils.model_mixins import ReferenceMixin, NameMixin


class WorkTechnology(NameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Технология работы'
        verbose_name_plural = 'Технологии работ'
