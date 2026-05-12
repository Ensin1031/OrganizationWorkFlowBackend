from django.db import models

from permissions.models import ACLModelMixin
from utils.model_mixins import (
    IsActiveMixin, SlugMixin, UniqueNameMixin, DescriptionMixin,
    CreatedUpdatedMixin, StartEndDatesMixin, ColorFieldMixin,
)


class Sprint(
    UniqueNameMixin, DescriptionMixin, IsActiveMixin, SlugMixin,
    ColorFieldMixin, StartEndDatesMixin, CreatedUpdatedMixin, ACLModelMixin,
):
    in_work = models.BooleanField(
        "Спринт в работе, активен", default=False, blank=True, db_index=True,
    )
    is_completed = models.BooleanField(
        "Спринт завершен", default=False, blank=True, db_index=True,
    )

    class Meta:
        verbose_name = 'Спринт'
        verbose_name_plural = 'Спринты'

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_completed:
            self.in_work = True
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
