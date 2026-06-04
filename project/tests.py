from django.urls import reverse
from rest_framework import status

from project.factories import (
    ProjectFactory, ProjectStatusFactory, ProjectVersionFactory, ProjectCategoryFactory, ProjectTypeFactory,
)
from utils.test_admin import TestAdmin, get_admin_change_view_url, get_admin_list_view_url, ACLViewSetTestCase


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


class ProjectViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.category = ProjectCategoryFactory()
        cls.type = ProjectTypeFactory()
        cls.project = ProjectFactory(category=cls.category, type=cls.type, manage_by=cls.user)

    def test_unauthorized_list(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,)

    def test_list_without_view_permission(self):
        self.authenticate(self.user)
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    def test_list_with_view_permission(self):
        self.grant_permission('view_project')
        self.authenticate(self.user)

        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_without_view_permission(self):
        self.authenticate(self.user)
        response = self.client.get(reverse('project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_view_permission(self):
        self.grant_permission('view_project')
        self.authenticate(self.user)

        response = self.client.get(reverse('project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_permission(self):
        self.grant_permission('view_project')
        self.authenticate(self.user)

        response = self.client.post(
            reverse('project-list'),
            {'name': 'New project', 'category_id': self.category.id, 'type_id': self.type.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_permission(self):
        self.grant_permission('view_project')
        self.grant_permission('add_project')
        self.authenticate(self.user)

        response = self.client.post(
            reverse('project-list'),
            {'name': 'New project', 'category_id': self.category.id, 'type_id': self.type.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_without_permission(self):
        self.grant_permission('view_project')
        self.authenticate(self.user)

        response = self.client.patch(
            reverse('project-detail', kwargs={'slug': self.project.slug}),
            {'name': 'Updated'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_permission(self):
        self.grant_permission('view_project')
        self.grant_permission('change_project')
        self.authenticate(self.user)

        response = self.client.patch(
            reverse('project-detail', kwargs={'slug': self.project.slug}),
            {'name': 'Updated'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_without_permission(self):
        self.grant_permission('view_project')
        self.authenticate(self.user)

        response = self.client.delete(reverse('project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_permission(self):
        self.grant_permission('view_project')
        self.grant_permission('delete_project')
        self.authenticate(self.user)

        response = self.client.delete(reverse('project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_false(self):
        self.authenticate(self.user)

        response = self.client.get(reverse('project-can-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['can_create'])

    def test_can_create_true(self):
        self.grant_permission('add_project')
        self.authenticate(self.user)

        response = self.client.get(reverse('project-can-create'))
        self.assertTrue(response.data['can_create'])

    def test_superuser_has_full_access(self):
        self.authenticate(self.superuser)

        response = self.client.patch(
            reverse('project-detail', kwargs={'slug': self.project.slug}),
            {'name': 'Changed by admin'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
