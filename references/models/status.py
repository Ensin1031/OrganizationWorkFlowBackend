from utils.model_mixins import ReferenceMixin, NameMixin


class StatusRow(NameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
