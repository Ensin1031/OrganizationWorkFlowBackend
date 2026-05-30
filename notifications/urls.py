from django.urls import path, include
from rest_framework.routers import DefaultRouter

from notifications.api.rest_view import NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]
