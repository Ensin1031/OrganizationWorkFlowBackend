from django.conf import settings
from django.db import models

from project.models import Project, ProjectStatus, ProjectVersion
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType
from sprint.models import Sprint
from utils.model_mixins import (
    UniqueNameMixin, IsActiveMixin, StartEndDatesMixin, DescriptionMixin, ColorFieldMixin,
    CreatedUpdatedMixin, SVGTextIconMixin,
)


class Work(
    UniqueNameMixin, DescriptionMixin, IsActiveMixin, ColorFieldMixin,
    SVGTextIconMixin, CreatedUpdatedMixin, StartEndDatesMixin,
):
    epic = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Эпик', related_name='epic_works',
    )
    histories = models.ManyToManyField(
        'self', symmetrical=False, blank=True, verbose_name='Истории', related_name='history_works',
    )
    type = models.ForeignKey(
        WorkType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип работы', related_name='works',
    )
    priority = models.ForeignKey(
        WorkPriority, on_delete=models.PROTECT, verbose_name='Приоритет', related_name='works',
    )
    tags = models.ManyToManyField(
        WorkTag, blank=True, verbose_name='Теги', related_name='works',
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Проект', related_name='works',
    )
    sprint = models.ForeignKey(
        Sprint, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Спринт', related_name='works',
    )
    status = models.ForeignKey(
        ProjectStatus, on_delete=models.PROTECT, verbose_name='Статус', related_name='works',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Создал', related_name='works_created',
    )
    execute_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Исполнитель', related_name='works_executed',
    )
    difficulty = models.ForeignKey(
        WorkDifficulty, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Сложность', related_name='works',
    )
    technology = models.ForeignKey(
        WorkTechnology, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Технология', related_name='works',
    )
    versions = models.ManyToManyField(
        ProjectVersion, blank=True, verbose_name='Версии', related_name='works',
    )
    target_start_date = models.DateField(verbose_name='Необходимо начать с', blank=True, null=True)
    target_end_date = models.DateField(verbose_name='Необходимо закончить до', blank=True, null=True)
    lead_time = models.DurationField(verbose_name='Первоначальная оценка времени выполнения', null=True, blank=True)
    wasted_time = models.DurationField(verbose_name='Времени потрачено на выполнение', null=True, blank=True)
    slug = models.SlugField(
        max_length=50, verbose_name='Код (slug) работы', blank=True, default='', db_index=True,
    )

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return f"{self.slug or self.name}"

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if not self.slug:
            self.refresh_from_db()
            self.slug = f'{self.project.code_prefix}-{self.pk}'.upper()
            self.save(update_fields=['slug'])
