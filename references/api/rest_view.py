from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from permissions.api.mixins import ACLViewSetMixin
from references.api.serializers import (
    StatusRowSerializer, WorkDifficultySerializer, WorkPrioritySerializer, WorkTagSerializer, WorkTechnologySerializer,
    WorkTypeSerializer,
)
from references.models.status import StatusRow
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType


class ReferencesViewSetMixin(ACLViewSetMixin):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    http_method_names = ['get', 'post', 'patch', 'delete']

    search_fields = ['name',]
    ordering_fields = ['name', 'created', 'updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.queryset is None:
            raise AssertionError("queryset must be defined")
        queryset = super().get_queryset().filter(is_active=True).order_by('-updated')
        return queryset


class StatusRowViewSet(ReferencesViewSetMixin):
    queryset = StatusRow.objects.all()
    serializer_class = StatusRowSerializer
    pagination_class = None


class WorkDifficultyViewSet(ReferencesViewSetMixin):
    queryset = WorkDifficulty.objects.all()
    serializer_class = WorkDifficultySerializer


class WorkPriorityViewSet(ReferencesViewSetMixin):
    queryset = WorkPriority.objects.all()
    serializer_class = WorkPrioritySerializer


class WorkTagViewSet(ReferencesViewSetMixin):
    queryset = WorkTag.objects.all()
    serializer_class = WorkTagSerializer


class WorkTechnologyViewSet(ReferencesViewSetMixin):
    queryset = WorkTechnology.objects.all()
    serializer_class = WorkTechnologySerializer


class WorkTypeViewSet(ReferencesViewSetMixin):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
