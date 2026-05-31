from channels.db import database_sync_to_async
from django.db import models
from django.db.models import QuerySet

from users.models import UserExtended
from utils.model_mixins import CreatedUpdatedMixin, IsActiveMixin, DescriptionMixin, SlugMixin


class Notification(DescriptionMixin, CreatedUpdatedMixin, IsActiveMixin, SlugMixin):
    """ Модель отправляемых сообщений """

    user = models.ForeignKey(
        UserExtended, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='notifications',
    )
    title = models.CharField("Заголовок", max_length=255, blank=True)
    is_read = models.BooleanField("Активен", default=False, blank=True, db_index=True)
    payload = models.JSONField('Данные сообщения', default=dict, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ('-created', 'user')

    def __str__(self):
        return f'Сообщение пользователю {self.user} ot {self.created}'

    @classmethod
    def get_rows_by_user(cls, user: UserExtended) -> QuerySet['Notification']:
        return cls.objects.filter(user=user)

    @classmethod
    def get_unread_count(cls, user: UserExtended) -> int:
        return cls.get_rows_by_user(user=user).filter(is_read=False, is_active=True).only('id').count()

    @classmethod
    @database_sync_to_async
    def get_async_unread_count(cls, user: UserExtended) -> int:
        return cls.get_unread_count(user=user)
