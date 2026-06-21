from django.urls import reverse
from rest_framework import status

from comments.factories import WorkCommentFactory
from comments.models import WorkComment
from users.factories import UserExtendedFactory
from utils.test_admin import get_admin_list_view_url, get_admin_change_view_url, TestAdmin, ACLViewSetTestCase
from work.factories import WorkFactory


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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_view_loads_normally_for_work_comment_add(self):
        """Проверка доступа на страницу списка экземпляров модели в админке"""

        # логинимся под суперпользователем
        self.client.login(email=self.super_user.email, password=self.password)

        response = self.client.get(get_admin_list_view_url(self.work_comment))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkCommentViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.work = WorkFactory()
        cls.comment = WorkCommentFactory(work=cls.work, created_by=cls.user)
        cls.child_comment = WorkCommentFactory(work=cls.work, created_by=cls.user, parent=cls.comment)

    def test_list_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_list_with_permission(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_without_permission(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("comments-detail", kwargs={"slug": self.comment.slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_permission(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.get(reverse("comments-detail", kwargs={"slug": self.comment.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_permission(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("comments-list"),
            {"description": "new comment", "created_by_id": self.user.id, "work_id": self.work.slug},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_permission(self):
        self.grant_permission("view_workcomment")
        self.grant_permission("add_workcomment")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("comments-list"),
            {"description": "new comment", "created_by_id": self.user.id, "work_id": self.work.slug},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(WorkComment.objects.filter(description="new comment").exists())

    def test_create_child_comment(self):
        self.grant_permission("view_workcomment")
        self.grant_permission("add_workcomment")
        self.authenticate(self.user)

        response = self.client.post(
            reverse("comments-list"),
            {
                "description": "reply",
                "created_by_id": self.user.id,
                "work_id": self.work.slug,
                "parent_id": self.comment.slug,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_without_permission(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("comments-detail", kwargs={"slug": self.comment.slug}),
            {"description": "updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_permission(self):
        self.grant_permission("view_workcomment")
        self.grant_permission("change_workcomment")
        self.authenticate(self.user)

        response = self.client.patch(
            reverse("comments-detail", kwargs={"slug": self.comment.slug}),
            {"description": "updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.description, "updated")

    def test_delete_without_permission(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.delete(reverse("comments-detail", kwargs={"slug": self.comment.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_permission(self):
        self.grant_permission("view_workcomment")
        self.grant_permission("delete_workcomment")
        self.authenticate(self.user)

        response = self.client.delete(reverse("comments-detail", kwargs={"slug": self.comment.slug}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_work(self):
        self.grant_permission("view_workcomment")

        other_work = WorkFactory()
        WorkCommentFactory(work=other_work, created_by=self.user)

        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"), {"work": self.work.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_parent(self):
        self.grant_permission("view_workcomment")
        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"), {"parent": self.comment.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_by_created_by(self):
        self.grant_permission("view_workcomment")

        other_user = UserExtendedFactory()
        WorkCommentFactory(work=self.work, created_by=other_user,)

        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"), {"created_by": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search(self):
        self.grant_permission("view_workcomment")

        self.comment.description = "UniqueText123"
        self.comment.save()

        self.authenticate(self.user)

        response = self.client.get(reverse("comments-list"), {"search": "UniqueText123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_superuser_has_full_access(self):
        self.authenticate(self.superuser)

        response = self.client.patch(
            reverse("comments-detail", kwargs={"slug": self.comment.slug}),
            {"description": "edited by admin"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
