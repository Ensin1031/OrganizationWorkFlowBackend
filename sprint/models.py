from utils.model_mixins import (
    IsActiveMixin, SlugMixin, UniqueNameMixin, DescriptionMixin,
    CreatedUpdatedMixin, StartEndDatesMixin, ColorFieldMixin,
)


class Sprint(
    UniqueNameMixin, DescriptionMixin, IsActiveMixin, SlugMixin,
    ColorFieldMixin, StartEndDatesMixin, CreatedUpdatedMixin,
):

    class Meta:
        verbose_name = 'Спринт'
        verbose_name_plural = 'Спринты'
