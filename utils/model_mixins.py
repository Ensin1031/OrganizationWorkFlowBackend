from django.db import models


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField("Дата создания", auto_now_add=True, blank=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True, blank=True, db_index=True)

    class Meta:
        abstract = True
