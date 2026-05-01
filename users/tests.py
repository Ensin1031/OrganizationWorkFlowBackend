from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin


class UsersAdminTest(TestAdmin):
    """Тест приложения Users для админки"""
    def setUp(self) -> None:
        super().setUp()

    def test_change_view_loads_normally_for_users_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        # проверяем модель AccessGroup
        response = self.client.get(get_admin_change_view_url(self.super_user))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_users_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.super_user))
        self.assertEqual(response.status_code, 200)
