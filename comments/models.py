from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from utils.model_mixins import CreatedUpdatedMixin, IsActiveMixin, SlugMixin, DescriptionMixin
from work.models.work import Work


class WorkComment(MPTTModel, DescriptionMixin, IsActiveMixin, SlugMixin, CreatedUpdatedMixin):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments',
    )
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, verbose_name='Работа', related_name='comments',
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, db_index=True,
        verbose_name='Родительский комментарий', related_name='children',
    )

    class MPTTMeta:
        order_insertion_by = ['-created']

    class Meta:
        verbose_name = 'Комментарий к работе'
        verbose_name_plural = 'Комментарии к работам'
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return f"Комментарий #{self.pk} ({self.work.name}): {self.description[:10]}"
