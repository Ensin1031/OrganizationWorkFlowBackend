from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from permissions.api.mixins import ACLViewSetMixin
from project.api.serializers import (
    ProjectSerializer, ProjectCategorySerializer, ProjectTypeSerializer,
    ProjectStatusSerializer, ProjectVersionSerializer,
)
from project.models import Project, ProjectCategory, ProjectType, ProjectStatus, ProjectVersion


class ProjectViewSet(ACLViewSetMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['name', 'code_prefix']

    filterset_fields = {
        'category': ['exact'],
        'type': ['exact'],
        'manage_by': ['exact'],
    }
    ordering_fields = ['name', 'code_prefix']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-updated')
        return queryset


class ProjectCategoriesViewSet(ACLViewSetMixin):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-updated')
        return queryset


class ProjectTypesViewSet(ACLViewSetMixin):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-updated')
        return queryset


class ProjectStatusViewSet(ACLViewSetMixin):
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = {
        'status': ['exact'],
        'project': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        return queryset


class ProjectVersionViewSet(ACLViewSetMixin):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = {
        'project': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        return queryset
