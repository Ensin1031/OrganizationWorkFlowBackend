from django.urls import path, include
from rest_framework.routers import DefaultRouter

from references.api.rest_view import (
    StatusRowViewSet, WorkDifficultyViewSet, WorkPriorityViewSet, WorkTagViewSet, WorkTechnologyViewSet,
    WorkTypeViewSet,
)

router = DefaultRouter()
router.register(r'statuses', StatusRowViewSet, basename='statuses')
router.register(r'difficulties', WorkDifficultyViewSet, basename='difficulties')
router.register(r'priorities', WorkPriorityViewSet, basename='priorities')
router.register(r'tags', WorkTagViewSet, basename='tags')
router.register(r'technologies', WorkTechnologyViewSet, basename='technologies')
router.register(r'work-types', WorkTypeViewSet, basename='work-types')

urlpatterns = [
    path('', include(router.urls)),
]
