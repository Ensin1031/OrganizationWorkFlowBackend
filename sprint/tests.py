from sprint.factories import SprintFactory
from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin


class ReferencesAdminTest(TestAdmin):
    """ Тест приложения sprint для админки """
    def setUp(self) -> None:
        super().setUp()
        self.sprint = SprintFactory()

    def test_change_view_loads_normally_for_sprint_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.sprint))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_sprint_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.sprint))
        self.assertEqual(response.status_code, 200)
