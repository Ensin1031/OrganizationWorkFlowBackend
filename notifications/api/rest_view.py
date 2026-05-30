from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from notifications.api.serializers import NotificationSerializer
from notifications.models import Notification


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['title',]

    filterset_fields = [
        'is_read',
        'is_active',
        'user',
    ]

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_active=True,
            user_id=self.request.user.pk,
        ).order_by('is_read', '-created')
        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        user = self.request.user
        if user.is_authenticated:
            response.data['unread_count'] = Notification.get_unread_count(user=user)
        return response

    @action(detail=False, methods=["GET"], url_path="unread", url_name="unread")
    def get_unread(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        if user.is_authenticated:
            response_data = {'unread_count': Notification.get_unread_count(user=user)}
        else:
            response_data = {'unread_count': 0}
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="delete-all", url_name="delete-all")
    def post_delete_all(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        if user.is_authenticated:
            Notification.get_rows_by_user(user=user).delete()
            response_data = {'unread_count': Notification.get_unread_count(user=user)}
        else:
            response_data = {'unread_count': 0}
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="mark-as-read", url_name="mark-as-read")
    def post_mark_as_read(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        notification = self.get_object()
        if user.is_authenticated:
            notification.is_read = True
            notification.save(update_fields=['is_read'])
            notification.refresh_from_db()
            response_data = {
                **NotificationSerializer(notification, many=False, context={'request': request}).data,
                'unread_count': Notification.get_unread_count(user=user),
            }
        else:
            response_data = {'unread_count': 0}
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="mark-all-as-read", url_name="mark-all-as-read")
    def post_mark_all_as_read(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        if user.is_authenticated:
            Notification.get_rows_by_user(user=user).update(is_read=True)
            response_data = {
                'unread_count': Notification.get_unread_count(user=user),
            }
        else:
            response_data = {'unread_count': 0}
        return Response(response_data, status=status.HTTP_200_OK)
