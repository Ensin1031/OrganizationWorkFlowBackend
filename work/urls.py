from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work.api.rest_view import WorkViewSet, WorkConnectionViewSet

router = DefaultRouter()
router.register(r'works', WorkViewSet, basename='works')
router.register(r'work-connections', WorkConnectionViewSet, basename='work-connections')

urlpatterns = [
    path('', include(router.urls)),
]
