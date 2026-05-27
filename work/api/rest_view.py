from django.db.models import F, CharField, Case, When, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.api.mixins import ACLViewSetMixin
from utils.choices.work_connection_choices import REVERSE_TYPES
from work.api.filters import WorkFilter, WorkConnectionFilter
from work.api.serializers import WorkSerializer, WorkConnectionSerializer
from work.models.work import Work
from work.models.work_connection import WorkConnection


class WorkViewSet(ACLViewSetMixin):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    filterset_class = WorkFilter

    search_fields = ['name', 'slug']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_active=True
        ).select_related(
            'epic', 'type', 'priority', 'project', 'sprint',
            'status', 'created_by', 'execute_by', 'difficulty', 'technology',
        ).order_by('-slug', '-updated')
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('created_by_id'):
            try:
                request.data._mutable = True
            except AttributeError:
                pass
            request.data['created_by_id'] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["GET"], url_path="by-sprints", url_name="by-sprints")
    def get_by_sprints(self, request, *args, **kwargs) -> Response:
        qs = self.get_queryset().filter(is_active=True).select_related('sprint', 'project')
        sprints = request.query_params.getlist('sprints')
        without_types = request.query_params.getlist('without_types')
        if sprints:
            qs = qs.filter(sprint__slug__in=sprints).distinct()
            if without_types:
                qs = qs.exclude(type_id__in=without_types)
        else:
            qs = qs.none()
        return Response(
            WorkSerializer(qs, many=True, context={'request': request}).data,
            status=status.HTTP_200_OK,
        )


class WorkConnectionViewSet(ACLViewSetMixin):
    queryset = WorkConnection.objects.all()
    serializer_class = WorkConnectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None

    filterset_class = WorkConnectionFilter

    ordering_fields = ['id', 'type']
    ordering = ['type']

    def get_queryset(self):
        queryset = super().get_queryset()

        work_slug = self.request.query_params.get('work')

        if work_slug:
            reverse_type_cases = [
                When(type=from_type, then=Value(to_type))
                for from_type, to_type in REVERSE_TYPES.items()
            ]

            queryset = queryset.annotate(
                name=Case(
                    When(
                        work_to__slug=work_slug,
                        then=Concat(
                            Value('['),
                            F('work_from__slug'),
                            Value('] '),
                            F('work_from__name'),
                            output_field=CharField(),
                        ),
                    ),
                    When(
                        work_from__slug=work_slug,
                        then=Concat(
                            Value('['),
                            F('work_to__slug'),
                            Value('] '),
                            F('work_to__name'),
                            output_field=CharField(),
                        ),
                    ),
                    output_field=CharField(),
                ),
                slug=Case(
                    When(work_to__slug=work_slug, then=F('work_from__slug')),
                    When(work_from__slug=work_slug, then=F('work_to__slug')),
                    output_field=CharField(),
                ),
                type_id=Case(
                    When(work_to__slug=work_slug, then=F('type')),
                    When(
                        work_from__slug=work_slug,
                        then=Case(*reverse_type_cases, output_field=CharField()),
                    ),
                    output_field=CharField(),
                ),
            )

        return queryset.select_related('work_from', 'work_to').order_by('type')
