from copy import copy

from django.db.models import Case, When, Value, IntegerField, Sum, F, CharField
from django.db.models.functions import Concat, Trim
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.api.mixins import ACLViewSetMixin
from sprint.api.serializers import (
    SprintSerializer, SprintUserLoadSerializer, SprintWithoutUsersLeadTimeSerializer, SprintShortSerializer,
)
from sprint.models import Sprint
from work.api.filters import WorkFilter


class SprintViewSet(ACLViewSetMixin):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['name',]

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    filterset_fields = [
        'is_completed',
        'in_work',
    ]

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_active=True
        ).annotate(
            sort_order=Case(
                When(in_work=True, is_completed=False, then=Value(1)),
                When(in_work=False, is_completed=False, then=Value(2)),
                When(in_work=True, is_completed=True, then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('sort_order', '-updated')
        return queryset

    @action(detail=True, methods=["GET"], url_path="users-load", url_name="users-load")
    def sprint_users_load(self, request, *args, **kwargs) -> Response:
        sprint = self.get_object()

        query_params = copy(request.query_params)

        filtered_queryset = WorkFilter(
            data=query_params,
            queryset=sprint.works.filter(is_active=True),
            request=request,
        ).qs

        users = filtered_queryset.filter(
            execute_by__isnull=False,
        ).annotate(
            user_id=F('execute_by_id'),
            user_email=F('execute_by__email'),
            user_photo=F('execute_by__profile_photo'),
            full_name_raw=Trim(
                Concat(
                    F('execute_by__last_name'),
                    Value(' '),
                    F('execute_by__first_name'),
                    Value(' '),
                    F('execute_by__second_name'),
                    output_field=CharField(),
                )
            ),
        ).annotate(
            user_full_name=Case(
                When(
                    full_name_raw='',
                    then=F('execute_by__username'),
                ),
                default=F('full_name_raw'),
                output_field=CharField(),
            ),
        ).values(
            'user_id',
            'user_email',
            'user_photo',
            'user_full_name',
        ).annotate(
            user_lead_time=Sum('lead_time'),
        ).order_by('-user_full_name')

        without_users = filtered_queryset.filter(
            execute_by__isnull=True,
        ).aggregate(
            total_lead_time=Sum('lead_time'),
        )

        return Response({
            'users': SprintUserLoadSerializer(users, many=True, context={'request': request}).data,
            'without_users': SprintWithoutUsersLeadTimeSerializer(without_users, context={'request': request}).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="active", url_name="active")
    def get_active_sprints(self, request, *args, **kwargs) -> Response:
        return Response(
            SprintShortSerializer(
                self.get_queryset().filter(is_completed=False, in_work=True),
                many=True,
            ).data,
            status=status.HTTP_200_OK,
        )
