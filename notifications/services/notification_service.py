from typing import Union

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail  # noqa

from notifications.api.serializers import NotificationSerializer
from notifications.models import Notification
from users.models import UserExtended
from utils.choices.work_notification_types_choices import WorkNotificationType


class NotificationService:

    @classmethod
    def send(
        cls, *,
        user: UserExtended,
        notification_type: Union[WorkNotificationType, str],
        title: str,
        message: str,
        payload=None,
        send_email=True,
    ):
        notification = Notification.objects.create(
            user=user,
            title=title,
            description=message,
            payload=payload or {},
        )
        unread_count = Notification.get_unread_count(user=user)

        if user.need_send_email_notification and send_email and user.email:
            send_mail(
                subject=title,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True
            )

        if user.need_send_push_notification:
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f'user_{user.pk}',
                {
                    'type': 'notify',
                    'send_type': notification_type,
                    'unread_count': unread_count,
                    'data': NotificationSerializer(notification, many=False).data,
                }
            )

        return notification
