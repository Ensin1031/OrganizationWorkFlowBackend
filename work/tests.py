from utils.test_admin import TestAdmin, get_admin_change_view_url, get_admin_list_view_url
from work.factories import WorkFactory, WorkConnectionFactory


class WorkAdminTest(TestAdmin):
    """ Тест приложения work для админки """
    def setUp(self) -> None:
        super().setUp()
        self.work = WorkFactory()
        self.work_connection = WorkConnectionFactory()

    def test_change_view_loads_normally_for_work_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.work))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.work_connection))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_work_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.work))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.work_connection))
        self.assertEqual(response.status_code, 200)
