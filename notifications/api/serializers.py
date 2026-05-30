from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notification
        exclude = ('is_active', 'updated')
