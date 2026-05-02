from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.api.rest_view import (
    ProjectViewSet, ProjectCategoriesViewSet, ProjectTypesViewSet, ProjectStatusViewSet, ProjectVersionViewSet,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-categories', ProjectCategoriesViewSet, basename='project-category')
router.register(r'project-types', ProjectTypesViewSet, basename='project-type')
router.register(r'project-statuses', ProjectStatusViewSet, basename='project-statuses')
router.register(r'project-versions', ProjectVersionViewSet, basename='project-versions')

urlpatterns = [
    path('', include(router.urls)),
]
