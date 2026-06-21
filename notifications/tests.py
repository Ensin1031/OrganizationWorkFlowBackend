from django.urls import reverse
from rest_framework import status

from notifications.models import Notification
from users.factories import UserExtendedFactory
from utils.test_admin import ACLViewSetTestCase


class NotificationViewSetTestCase(ACLViewSetTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.other_user = UserExtendedFactory(email="other@test.ru", password=cls.password)

        cls.notification_1 = Notification.objects.create(
            user=cls.user,
            title="Notification 1",
            description="Test",
            is_read=False,
        )

        cls.notification_2 = Notification.objects.create(
            user=cls.user,
            title="Notification 2",
            description="Test",
            is_read=True,
        )

        cls.other_notification = Notification.objects.create(
            user=cls.other_user,
            title="Other notification",
            description="Test",
            is_read=False,
        )

    def test_unauthorized_list(self):
        response = self.client.get(reverse("notifications-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_user_notifications(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {item["id"] for item in response.data["results"]}
        self.assertEqual(ids, {self.notification_1.pk, self.notification_2.pk})

    def test_list_contains_unread_count(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-list"))
        self.assertEqual(response.data["unread_count"], 1)

    def test_retrieve_own_notification(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-detail", kwargs={"pk": self.notification_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_foreign_notification(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-detail", kwargs={"pk": self.other_notification.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_count(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-unread"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 1)

    def test_mark_as_read(self):
        self.authenticate(self.user)

        response = self.client.post(
            reverse("notifications-mark-as-read", kwargs={"pk": self.notification_1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification_1.refresh_from_db()
        self.assertTrue(self.notification_1.is_read)
        self.assertEqual(response.data["unread_count"], 0)

    def test_mark_foreign_notification_as_read(self):
        self.authenticate(self.user)

        response = self.client.post(
            reverse("notifications-mark-as-read", kwargs={"pk": self.other_notification.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_all_as_read(self):
        Notification.objects.create(
            user=self.user,
            title="Unread",
            description="Test",
            is_read=False,
        )

        self.authenticate(self.user)

        response = self.client.post(reverse("notifications-mark-all-as-read"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 0)
        self.assertFalse(Notification.objects.filter(user=self.user, is_read=False).exists())

    def test_delete_all(self):
        self.authenticate(self.user)

        response = self.client.post(reverse("notifications-delete-all"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 0)
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 0)

    def test_delete_all_does_not_affect_other_users(self):
        self.authenticate(self.user)

        self.client.post(reverse("notifications-delete-all"))
        self.assertTrue(Notification.objects.filter(pk=self.other_notification.pk).exists())

    def test_create_notification(self):
        self.authenticate(self.user)

        response = self.client.post(
            reverse("notifications-list"),
            {"title": "Created", "description": "Text", "user": self.user.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_notification(self):
        self.authenticate(self.user)

        response = self.client.delete(reverse("notifications-detail", kwargs={"pk": self.notification_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_unread(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-list"), {"is_read": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_by_title(self):
        self.authenticate(self.user)

        response = self.client.get(reverse("notifications-list"), {"search": "Notification 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
