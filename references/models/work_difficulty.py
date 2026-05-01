from utils.model_mixins import NameMixin, ReferenceMixin


class WorkDifficulty(NameMixin, ReferenceMixin):

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложностей'
