from django.urls import reverse
from rest_framework import status

from utils.test_admin import TestAdmin, get_admin_change_view_url, get_admin_list_view_url, ACLViewSetTestCase
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


class WorkViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.work = WorkFactory(created_by=cls.user)

    def test_list_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("works-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_list_with_permission(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.get(reverse("works-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("works-detail", kwargs={"slug": self.work.slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_permission(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.get(reverse("works-detail", kwargs={"slug": self.work.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_permission(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("works-list"),
            {
                "name": "Новая задача",
                "priority_id": self.work.priority.id,
                "project_id": self.work.project.id,
                "status_id": self.work.status.id,
                "type_id": self.work.type.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_permission(self):
        self.grant_permission("view_work")
        self.grant_permission("add_work")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("works-list"),
            {
                "name": "Новая задача",
                "priority_id": self.work.priority.id,
                "project_id": self.work.project.id,
                "status_id": self.work.status.id,
                "type_id": self.work.type.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_without_permission(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("works-detail", kwargs={"slug": self.work.slug}),
            {"name": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_permission(self):
        self.grant_permission("view_work")
        self.grant_permission("change_work")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("works-detail", kwargs={"slug": self.work.slug}),
            {"name": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_without_permission(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.delete(reverse("works-detail", kwargs={"slug": self.work.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_permission(self):
        self.grant_permission("view_work")
        self.grant_permission("delete_work")
        self.authenticate(self.user)

        response = self.client.delete(reverse("works-detail", kwargs={"slug": self.work.slug}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_by_sprints(self):
        self.grant_permission("view_work")
        self.authenticate(self.user)

        response = self.client.get(reverse("works-by-sprints"), {"sprints": [self.work.sprint.slug]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkConnectionViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.work_from = WorkFactory()
        cls.work_to = WorkFactory()
        cls.connection = WorkConnectionFactory(work_from=cls.work_from, work_to=cls.work_to)

    def test_list_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("work-connections-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_with_permission(self):
        self.grant_permission("view_workconnection")
        self.authenticate(self.user)

        response = self.client.get(reverse("work-connections-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("work-connections-detail", kwargs={"pk": self.connection.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_permission(self):
        self.grant_permission("view_workconnection")
        self.authenticate(self.user)

        response = self.client.get(reverse("work-connections-detail", kwargs={"pk": self.connection.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_permission(self):
        self.grant_permission("view_workconnection")
        self.grant_permission("add_workconnection")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("work-connections-list"),
            {"type": self.connection.type, "work_from_id": self.work_from.slug, "work_to_id": self.work_to.slug},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_with_permission(self):
        self.grant_permission("view_workconnection")
        self.grant_permission("delete_workconnection")
        self.authenticate(self.user)

        response = self.client.delete(reverse("work-connections-detail", kwargs={"pk": self.connection.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_work(self):
        self.grant_permission("view_workconnection")
        self.authenticate(self.user)

        response = self.client.get(reverse("work-connections-list"), {"work": self.work_from.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
