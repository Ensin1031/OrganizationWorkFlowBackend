from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comments.api.rest_view import WorkCommentViewSet

router = DefaultRouter()
router.register(r'comments', WorkCommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
