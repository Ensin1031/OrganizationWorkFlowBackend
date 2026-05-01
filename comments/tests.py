from comments.factories import WorkCommentFactory
from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin


class WorkCommentAdminTest(TestAdmin):
    """Тест приложения WorkComment для админки"""
    def setUp(self) -> None:
        super().setUp()
        self.work_comment = WorkCommentFactory()

    def test_change_view_loads_normally_for_work_comment_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.work_comment))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_work_comment_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.work_comment))
        self.assertEqual(response.status_code, 200)
