from typing import Dict

from rest_framework import serializers

from project.api.serializers import (
    ProjectShortSerializer, ProjectStatusShortSerializer, ProjectVersionShortSerializer,
)
from project.models import Project, ProjectStatus, ProjectVersion
from references.api.serializers import (
    WorkTypeShortSerializer, WorkPriorityShortSerializer, WorkTagShortSerializer, WorkDifficultyShortSerializer,
    WorkTechnologyShortSerializer,
)
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType
from sprint.api.serializers import SprintShortSerializer
from sprint.models import Sprint
from users.api.serializers import UserExtendedShortSerializer
from users.models import UserExtended
from work.models.work import Work
from work.models.work_connection import WorkConnection


class WorkShortSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Work
        fields = [
            'id', 'name', 'color', 'icon', 'slug', 'lead_time', 'wasted_time', 'full_name',
            'start_date', 'end_date', 'target_start_date', 'target_end_date',
        ]


class WorkConnectionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    slug = serializers.CharField(read_only=True)
    type_name = serializers.CharField(read_only=True, source='get_type_display')
    work_from = WorkShortSerializer(read_only=True, many=False)
    work_to = WorkShortSerializer(read_only=True, many=False)

    class Meta:
        model = WorkConnection
        fields = [
            'id', 'type', 'type_name', 'work_from', 'work_to',
        ]


class WorkSerializer(serializers.ModelSerializer):
    """ Сериализатор для задачи """

    epic = WorkShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    histories = WorkShortSerializer(many=True, read_only=True)
    type = WorkTypeShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    priority = WorkPriorityShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    tags = WorkTagShortSerializer(many=True, read_only=True)
    project = ProjectShortSerializer(many=False, read_only=True)
    sprint = SprintShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    status = ProjectStatusShortSerializer(many=False, read_only=True)
    created_by = UserExtendedShortSerializer(many=False, read_only=True)
    execute_by = UserExtendedShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    difficulty = WorkDifficultyShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    technology = WorkTechnologyShortSerializer(many=False, read_only=True, required=False, allow_null=True)
    versions = ProjectVersionShortSerializer(many=True, read_only=True)

    relations_from = WorkConnectionSerializer(many=True, read_only=True, source='connections_from')
    relations_to = WorkConnectionSerializer(many=True, read_only=True, source='connections_to')

    full_name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=UserExtended.objects.all(),
        source='created_by',
        write_only=True,
        required=True,
        allow_null=False,
    )

    execute_by_id = serializers.PrimaryKeyRelatedField(
        queryset=UserExtended.objects.all(),
        source='execute_by',
        write_only=True,
        required=False,
        allow_null=True,
    )
    priority_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkPriority.objects.all(),
        source='priority',
        write_only=True,
        required=True,
        allow_null=False,
    )
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
        required=True,
        allow_null=False,
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectStatus.objects.all(),
        source='status',
        write_only=True,
        required=True,
        allow_null=False,
    )
    sprint_id = serializers.PrimaryKeyRelatedField(
        queryset=Sprint.objects.all(),
        source='sprint',
        write_only=True,
        required=False,
        allow_null=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkType.objects.all(),
        source='type',
        write_only=True,
        required=True,
        allow_null=False,
    )
    epic_id = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(),
        source='epic',
        many=False,
        write_only=True,
        required=False,
        allow_null=True,
    )
    difficulty_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkDifficulty.objects.all(),
        source='difficulty',
        many=False,
        write_only=True,
        required=False,
        allow_null=True,
    )
    technology_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkTechnology.objects.all(),
        source='technology',
        many=False,
        write_only=True,
        required=False,
        allow_null=True,
    )
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=WorkTag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False,
    )
    histories_ids = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(),
        source='histories',
        many=True,
        write_only=True,
        required=False,
    )
    versions_ids = serializers.PrimaryKeyRelatedField(
        queryset=ProjectVersion.objects.all(),
        source='versions',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Work
        fields = [
            'id', 'name', 'description', 'color', 'icon', 'created', 'updated', 'start_date', 'end_date',
            'slug', 'epic', 'histories', 'type', 'priority', 'tags', 'project', 'sprint', 'status', 'full_name',
            'created_by', 'execute_by', 'difficulty', 'technology', 'versions', 'target_start_date', 'target_end_date',
            'lead_time', 'wasted_time',
            'relations_from', 'relations_to',
            'created_by_id', 'execute_by_id', 'priority_id', 'project_id', 'status_id', 'sprint_id', 'type_id',
            'epic_id', 'difficulty_id', 'technology_id', 'tags_ids', 'histories_ids', 'versions_ids',
        ]
        read_only_fields = ['slug', 'created', 'updated']

    def create(self, validated_data: Dict) -> Work:
        work: Work = super().create(validated_data)
        return work

    def update(self, instance: Work, validated_data: Dict) -> Work:
        work: Work = super().update(instance, validated_data)
        return work
