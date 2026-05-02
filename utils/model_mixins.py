import random

from colorfield.fields import ColorField
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from utils.custom_slugify import custom_slugify


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField("Дата создания", auto_now_add=True, blank=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class StartEndDatesMixin(models.Model):

    start_date = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    is_active = models.BooleanField("Активен", default=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class SVGTextIconMixin(models.Model):

    icon = models.TextField("SVG Изображение/иконка", blank=True)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField("Наименование", max_length=255, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UniqueNameMixin(models.Model):
    name = models.CharField("Наименование", max_length=255, blank=False, null=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DescriptionMixin(models.Model):
    description = CKEditor5Field("Описание", blank=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):

    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Слаг (URL) записи')

    class Meta:
        abstract = True

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            default_slug = 'item'
            slug_source = ''
            for field_name in ['name', 'description', 'username']:
                if hasattr(self, field_name):
                    value = getattr(self, field_name, None)
                    if value:
                        slug_source = str(value)
                        break
            if not slug_source:
                slug_source = default_slug
            base_slug = custom_slugify(slug_source)
            if not base_slug:
                base_slug = default_slug
            slug = base_slug
            counter = 1
            if self.pk:
                while self.__class__.objects.exclude(id=self.pk).filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
            else:
                while self.__class__.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
            self.slug = slug
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class ColorFieldMixin(models.Model):
    color = ColorField("Цвет", blank=True, null=True, help_text='Оставьте пустым для случайного выбора цвета')

    class Meta:
        abstract = True

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.color:
            color_palette = [
                "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD",
                "#D4A5A5", "#9B5DE5", "#F15BB5", "#FEE440", "#00BBF9",
                "#00F5D4", "#F7B801", "#F05454", "#8AC6D1", "#FFC2D1",
                "#A7E0E0", "#E2B1B1", "#B5E2FA", "#FF9E7A", "#C8E7D5"
            ]
            self.color = random.choice(color_palette)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class ReferenceMixin(
    DescriptionMixin, IsActiveMixin, SlugMixin, ColorFieldMixin, SVGTextIconMixin, CreatedUpdatedMixin,
):
    class Meta:
        abstract = True
