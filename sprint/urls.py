from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sprint.api.rest_view import SprintViewSet

router = DefaultRouter()
router.register(r'sprints', SprintViewSet, basename='sprints')

urlpatterns = [
    path('', include(router.urls)),
]
