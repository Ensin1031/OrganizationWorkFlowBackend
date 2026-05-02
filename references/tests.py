from references.factories import (
    WorkTagFactory, StatusRowFactory, WorkTechnologyFactory, WorkDifficultyFactory, WorkPriorityFactory,
    WorkTypeFactory,
)
from utils.test_admin import TestAdmin, get_admin_change_view_url, get_admin_list_view_url


class ReferencesAdminTest(TestAdmin):
    """Тест приложения References для админки"""
    def setUp(self) -> None:
        super().setUp()
        self.work_tag = WorkTagFactory()
        self.status_row = StatusRowFactory()
        self.work_technology = WorkTechnologyFactory()
        self.work_difficulty = WorkDifficultyFactory()
        self.work_priority = WorkPriorityFactory()
        self.work_type = WorkTypeFactory()

    def test_change_view_loads_normally_for_references_add(self):
        """Проверка доступа на страницу просмотра/редактирования экземпляра модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_change_view_url(self.work_tag))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.status_row))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.work_technology))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.work_difficulty))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.work_priority))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_change_view_url(self.work_type))
        self.assertEqual(response.status_code, 200)

    def test_list_view_loads_normally_for_references_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.work_tag))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.status_row))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.work_technology))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.work_difficulty))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.work_priority))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(get_admin_list_view_url(self.work_type))
        self.assertEqual(response.status_code, 200)
