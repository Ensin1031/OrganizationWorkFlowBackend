from typing import TYPE_CHECKING, Literal

from django.db import models

if TYPE_CHECKING:
    from users.models import UserExtended

PERMISSION_TYPE = Literal["add", "change", "view", "delete"]


class ACLModelMixin(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def _permission_name(cls, action: PERMISSION_TYPE) -> str:
        return f'{cls._meta.app_label}.{action}_{cls._meta.model_name}'

    @classmethod
    def can_create(cls, user: 'UserExtended', *args, **kwargs) -> bool:
        """ Разрешение на создание записи модели """
        if not user or not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        return user.has_perm(cls._permission_name('add'))

    def can_edit(self, user: 'UserExtended', *args, **kwargs) -> bool:
        """ Разрешение на редактирование записи модели """
        if not user or not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        return user.has_perm(self._permission_name('change'))

    def can_view(self, user: 'UserExtended', *args, **kwargs) -> bool:
        """ Разрешение на просмотр записи модели """
        if not user or not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        return user.has_perm(self._permission_name('view'))

    def can_delete(self, user: 'UserExtended', *args, **kwargs) -> bool:
        """ Разрешение на удаление записи модели """
        if not user or not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        return user.has_perm(self._permission_name('delete'))
