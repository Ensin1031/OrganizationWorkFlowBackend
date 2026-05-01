from django.db import models

from utils.choices.work_connection_choices import WorkConnectionType
from work.models.work import Work


class WorkConnection(models.Model):
    type = models.CharField(verbose_name="Тип связи", max_length=50, choices=WorkConnectionType)
    work_from = models.ForeignKey(
        Work, on_delete=models.CASCADE, verbose_name='Прикрепляемая работа', related_name='connections_from',
    )
    work_to = models.ForeignKey(
        Work, on_delete=models.CASCADE, verbose_name='Работа, к которой прикрепляем', related_name='connections_to',
    )

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = 'Связь работы'
        verbose_name_plural = 'Связи работ'
