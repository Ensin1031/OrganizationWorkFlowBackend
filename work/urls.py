from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work.api.rest_view import WorkViewSet

router = DefaultRouter()
router.register(r'works', WorkViewSet, basename='works')

urlpatterns = [
    path('', include(router.urls)),
]
