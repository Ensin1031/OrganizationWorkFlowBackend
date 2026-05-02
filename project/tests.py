from project.factories import ProjectFactory, ProjectStatusFactory, ProjectVersionFactory, ProjectCategoryFactory, \
    ProjectTypeFactory
from utils.test_admin import TestAdmin, get_admin_change_view_url, get_admin_list_view_url


class ProjectAdminTest(TestAdmin):
    """Тест приложения Project для админки"""
    def setUp(self) -> None:
        super().setUp()
        self.project = ProjectFactory()
        self.project_status = ProjectStatusFactory()
        self.project_version = ProjectVersionFactory()
        self.project_category = ProjectCategoryFactory()
        self.project_type = ProjectTypeFactory()

    def test_change_view_loads_normally_for_project_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.project))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.project_status))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.project_version))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.project_category))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.project_type))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_project_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.project))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.project_status))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.project_version))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.project_category))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.project_type))
        self.assertEqual(response.status_code, 200)
