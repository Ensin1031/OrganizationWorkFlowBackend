from typing import Optional

from django.db import models


class ACLModelMixin(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def can_create(cls, user_id: Optional[int], is_superuser: bool, *args, **kwargs) -> bool:
        """ Разрешение на создание записи модели """
        if is_superuser:
            return True
        # TODO Пока заглушка. Разрешаем всем авторизированным. Реализовать проверку прав доступа.
        return user_id is not None

    def can_edit(self, user_id: Optional[int], is_superuser: bool, *args, **kwargs) -> bool:
        """ Разрешение на редактирование записи модели """
        if is_superuser:
            return True
        # TODO Пока заглушка. Разрешаем всем авторизированным. Реализовать проверку прав доступа.
        return user_id is not None

    def can_view(self, user_id: Optional[int], is_superuser: bool, *args, **kwargs) -> bool:
        """ Разрешение на просмотр записи модели """
        if is_superuser:
            return True
        # TODO Пока заглушка. Разрешаем всем авторизированным. Реализовать проверку прав доступа.
        return user_id is not None
