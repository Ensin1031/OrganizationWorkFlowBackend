from datetime import timedelta

from django.urls import reverse
from rest_framework import status

from sprint.factories import SprintFactory
from users.factories import UserExtendedFactory
from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin, ACLViewSetTestCase
from work.factories import WorkFactory


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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_view_loads_normally_for_sprint_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.sprint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SprintViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sprint = SprintFactory(in_work=True, is_completed=False)

    def test_list_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_list_with_permission(self):
        self.grant_permission("view_sprint")
        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-detail", kwargs={"slug": self.sprint.slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_permission(self):
        self.grant_permission("view_sprint")
        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-detail", kwargs={"slug": self.sprint.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_permission(self):
        self.grant_permission("view_sprint")
        self.authenticate(self.user)

        response = self.client.post(reverse("sprints-list"), {"name": "Sprint API"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_permission(self):
        self.grant_permission("view_sprint")
        self.grant_permission("add_sprint")
        self.authenticate(self.user)

        response = self.client.post(reverse("sprints-list"), {"name": "Sprint API"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_without_permission(self):
        self.grant_permission("view_sprint")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("sprints-detail", kwargs={"slug": self.sprint.slug}),
            {"name": "Updated sprint"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_permission(self):
        self.grant_permission("view_sprint")
        self.grant_permission("change_sprint")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("sprints-detail", kwargs={"slug": self.sprint.slug}),
            {"name": "Updated sprint"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_without_permission(self):
        self.grant_permission("view_sprint")
        self.authenticate(self.user)

        response = self.client.delete(reverse("sprints-detail", kwargs={"slug": self.sprint.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_permission(self):
        self.grant_permission("view_sprint")
        self.grant_permission("delete_sprint")
        self.authenticate(self.user)

        response = self.client.delete(reverse("sprints-detail", kwargs={"slug": self.sprint.slug}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_active_sprints(self):
        self.grant_permission("view_sprint")

        SprintFactory(in_work=False, is_completed=False)
        SprintFactory(in_work=True, is_completed=True)

        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-active"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.sprint.id)

    def test_users_load(self):
        self.grant_permission("view_sprint")

        executor = UserExtendedFactory()
        WorkFactory(sprint=self.sprint, execute_by=executor, lead_time=timedelta(hours=5))
        WorkFactory(sprint=self.sprint, execute_by=None, lead_time=timedelta(hours=2))

        self.authenticate(self.user)

        response = self.client.get(reverse("sprints-users-load", kwargs={"slug": self.sprint.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)
        self.assertIn("without_users", response.data)
        self.assertEqual(len(response.data["users"]), 1)

    def test_superuser_has_full_access(self):
        self.authenticate(self.superuser)

        response = self.client.patch(
            reverse("sprints-detail", kwargs={"slug": self.sprint.slug}),
            {"name": "Changed by admin"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
