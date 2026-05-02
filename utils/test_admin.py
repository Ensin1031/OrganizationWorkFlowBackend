""" Вспомогательные методы для тестов на доступ в админку
Сделаны на базе: https://stackoverflow.com/questions/60322847/how-to-test-admin-change-views
"""
from django.test import TestCase

from django.db.models import Model
from django.urls import reverse
from django.test import Client

from users.factories import UserExtendedFactory


def get_admin_change_view_url(obj: Model) -> str:
    """
    Получение урла админки на страницу просмотра модели.
    """
    return reverse(
        'admin:{}_{}_change'.format(
            obj._meta.app_label,
            type(obj).__name__.lower()
        ),
        args=(obj.pk,)
    )


def get_admin_list_view_url(obj: Model) -> str:
    """
    Получение урла админки на страницу списка экземпляров модели.
    """
    return reverse(
        'admin:{}_{}_changelist'.format(
            obj._meta.app_label,
            type(obj).__name__.lower()
        ),
    )


def get_layer_sync_url() -> str:
    """ Получение урла синхронизации слоев карты """
    return reverse('admin:layer_layer_sync')


class TestAdmin(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.password = 'password'
        self.super_user = UserExtendedFactory(password=self.password, is_superuser=True, is_staff=True)
