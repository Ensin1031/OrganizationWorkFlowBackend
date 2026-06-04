""" Вспомогательные методы для тестов на доступ в админку
Сделаны на базе: https://stackoverflow.com/questions/60322847/how-to-test-admin-change-views
"""
from django.contrib.auth.models import Permission
from django.test import TestCase

from django.db.models import Model
from django.urls import reverse
from django.test import Client

from rest_framework.test import APITestCase

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


class ACLViewSetTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.password = 'StrongPassword123'
        cls.user = UserExtendedFactory(email='user@test.ru', password=cls.password, is_superuser=False)
        cls.superuser = UserExtendedFactory(
            email='admin@test.ru',
            password=cls.password,
            is_superuser=True,
            is_staff=True,
        )

    def authenticate(self, user):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'email': user.email, 'password': self.password},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def grant_permission(self, codename):
        permission = Permission.objects.get(codename=codename)
        self.user.user_permissions.add(permission)
