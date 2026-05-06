from typing import Optional

from django.conf import settings
from django.db import models

from permissions.models import ACLModelMixin
from references.models.status import StatusRow
from utils.model_mixins import (
    IsActiveMixin, UniqueNameMixin, SlugMixin, ColorFieldMixin, NameMixin, StartEndDatesMixin, CreatedUpdatedMixin,
    DescriptionMixin, SVGTextIconMixin,
)


class ProjectCategory(
    NameMixin, DescriptionMixin, IsActiveMixin, SlugMixin,
    ColorFieldMixin, SVGTextIconMixin, CreatedUpdatedMixin, ACLModelMixin,
):

    class Meta:
        verbose_name = 'Категория проекта'
        verbose_name_plural = 'Категории проектов'

    def has_projects(self) -> bool:
        return self.projects.only('id').exists()


class ProjectType(
    NameMixin, DescriptionMixin, IsActiveMixin, SlugMixin,
    ColorFieldMixin, SVGTextIconMixin, CreatedUpdatedMixin, ACLModelMixin,
):

    class Meta:
        verbose_name = 'Тип проекта'
        verbose_name_plural = 'Типы проектов'

    def has_projects(self) -> bool:
        return self.projects.only('id').exists()


class Project(
    UniqueNameMixin, DescriptionMixin, IsActiveMixin, SlugMixin, ColorFieldMixin,
    SVGTextIconMixin, CreatedUpdatedMixin, StartEndDatesMixin, ACLModelMixin,
):
    code_prefix = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Префикс кода задач проекта',
        help_text='Если оставить пустым, сгенерируется автоматически из имени'
    )
    manage_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Руководитель проекта', related_name='user_manage_projects',
    )
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Категория проекта', related_name='projects',
    )
    type = models.ForeignKey(
        ProjectType, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Тип проекта', related_name='projects',
    )
    urls = models.JSONField("Ссылки на ресурсы проекта", default=list, blank=True, null=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_base_prefix(self):
        if self.code_prefix and not Project.objects.exclude(pk=self.pk).filter(code_prefix=self.code_prefix).exists():
            return self.code_prefix.upper()
        elif self.slug:
            clean_base = self.slug
        else:
            default_code_prefix = 'proj'
            if self.name:
                code_prefix_source = self.name
            else:
                code_prefix_source = default_code_prefix
            from utils.custom_slugify import custom_slugify
            clean_base = custom_slugify(code_prefix_source)
            if not clean_base:
                clean_base = default_code_prefix

        for length in range(3, 11):
            candidate = clean_base[:length].upper()
            if not Project.objects.exclude(pk=self.pk).filter(code_prefix=candidate).exists():
                code_prefix = candidate
                break
        else:
            import random
            import string
            code_prefix = ''.join(random.choices(string.ascii_uppercase, k=4))
        code_prefix = code_prefix.upper()
        Project.objects.filter(id=self.pk).update(code_prefix=code_prefix)
        return code_prefix

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.code_prefix = self.get_base_prefix().upper()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_active_version(self) -> Optional['ProjectVersion']:
        return self.project_versions.filter(is_active=True, in_work=True).first()


class ProjectStatus(
    IsActiveMixin, ACLModelMixin,
):

    status = models.ForeignKey(
        StatusRow, on_delete=models.CASCADE, related_name='project_statuses', verbose_name='Статус'
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_statuses', verbose_name='Проект'
    )

    class Meta:
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проектов'

    def __str__(self):
        return str(self.status.name) + ' - ' + str(self.project.name)


class ProjectVersion(
    NameMixin, CreatedUpdatedMixin, StartEndDatesMixin, IsActiveMixin,
    ColorFieldMixin, DescriptionMixin, SlugMixin, ACLModelMixin,
):

    in_work = models.BooleanField(
        "Текущая рабочая версия", default=False, blank=True, db_index=True,
        help_text='В проекте может быть только одна. При установке - остальные скидываются.',
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_versions', verbose_name='Проект'
    )

    class Meta:
        verbose_name = 'Стадия / версия проекта'
        verbose_name_plural = 'Стадии / версии проектов'

    def __str__(self):
        return self.name + ' - ' + str(self.project.name)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.in_work:
            ProjectVersion.objects.exclude(id=self.pk).filter(in_work=True, project=self.project).update(in_work=False)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
