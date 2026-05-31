from typing import Optional, Dict

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from notifications.models import Notification
from users.models import UserExtended
from utils.choices.work_notification_types_choices import WorkNotificationType


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    async def connect(self):
        user: Optional[UserExtended] = self.scope['user']
        if not user or not user.is_authenticated:
            await self.close()
            return
        self.group_name = f'user_{user.pk}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_json({
            'type': WorkNotificationType.UNREAD_COUNT.value,
            'unread_count': await Notification.get_async_unread_count(user=user),
        })

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event: Dict):
        await self.send_json({
            'type': event.get('send_type'),
            'unread_count': event.get('unread_count'),
            'item': event.get('data'),
        })
