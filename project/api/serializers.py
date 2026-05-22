from typing import Dict, Optional

from rest_framework import serializers

from project.models import Project, ProjectVersion, ProjectStatus, ProjectCategory, ProjectType
from references.api.serializers import StatusRowSerializer
from users.api.serializers import UserSerializer
from users.models import UserExtended


class ProjectStatusShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='status.name', read_only=True)
    slug = serializers.CharField(source='status.slug', read_only=True)
    color = serializers.CharField(source='status.color', read_only=True)
    icon = serializers.CharField(source='status.icon', read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ['id', 'name', 'status', 'slug', 'color', 'icon', 'priority']


class ProjectStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(source='status.name', read_only=True)
    description = serializers.CharField(source='status.description', read_only=True)
    slug = serializers.CharField(source='status.slug', read_only=True)
    color = serializers.CharField(source='status.color', read_only=True)
    icon = serializers.CharField(source='status.icon', read_only=True)
    created = serializers.DateTimeField(source='status.created', read_only=True)
    updated = serializers.DateTimeField(source='status.updated', read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ['id', 'name', 'description', 'status', 'slug', 'color', 'icon', 'priority', 'created', 'updated']


class ProjectVersionShortSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = ProjectVersion
        fields = ['id', 'name', 'start_date', 'end_date', 'color', 'slug', 'in_work', 'project']


class ProjectVersionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProjectVersion
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date', 'color',
            'slug', 'in_work', 'created', 'updated', 'project', 'project_id',
        ]
        read_only_fields = ['slug', 'created', 'updated', 'project']


class ProjectCategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    has_projects = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'description', 'is_active', 'color', 'slug', 'has_projects', 'icon']


class ProjectTypeSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    has_projects = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectType
        fields = ['id', 'name', 'description', 'is_active', 'color', 'slug', 'has_projects', 'icon']


class ProjectShortSerializer(serializers.ModelSerializer):

    statuses = ProjectStatusSerializer(many=True, read_only=True, source='project_statuses')
    versions = ProjectVersionSerializer(many=True, read_only=True, source='project_versions')
    active_version = ProjectVersionSerializer(many=False, read_only=True, source='get_active_version')
    slug = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'color', 'icon', 'code_prefix', 'full_name',
            'start_date', 'end_date', 'statuses', 'versions', 'active_version',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """ Сериализатор для проекта """

    statuses = ProjectStatusSerializer(many=True, read_only=True, source='project_statuses')
    statuses_map = StatusRowSerializer(many=True, write_only=True, required=False, allow_null=True)

    versions = ProjectVersionSerializer(many=True, read_only=True, source='project_versions')
    active_version = ProjectVersionSerializer(many=False, read_only=True, source='get_active_version')
    set_active_version = ProjectVersionSerializer(many=False, write_only=True, required=False, allow_null=True)

    category = ProjectCategorySerializer(many=False, read_only=True, required=False, allow_null=True)
    type = ProjectTypeSerializer(many=False, read_only=True, required=False, allow_null=True)
    manage_by = UserSerializer(many=False, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(),
        source='type',
        write_only=True,
        required=False,
        allow_null=True
    )
    manage_by_id = serializers.PrimaryKeyRelatedField(
        queryset=UserExtended.objects.all(),
        source='manage_by',
        write_only=True,
        required=False,
        allow_null=True
    )

    slug = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'slug', 'color', 'icon', 'full_name',
            'code_prefix', 'is_active', 'category', 'type', 'manage_by', 'urls',
            'start_date', 'end_date', 'category_id', 'type_id', 'manage_by_id',
            'created', 'updated', 'versions', 'active_version', 'set_active_version',
            'statuses', 'statuses_map',
        ]
        read_only_fields = ['slug', 'created', 'updated']

    def create(self, validated_data):
        set_active_version = validated_data.pop('set_active_version', None)
        statuses_map = validated_data.pop('statuses_map', None)
        if validated_data.get('category_id', None) is None and validated_data.get('category', None) is None:
            validated_data['category_id'] = None
        if validated_data.get('type_id', None) is None and validated_data.get('type', None) is None:
            validated_data['type_id'] = None
        if validated_data.get('manage_by_id', None) is None and validated_data.get('manage_by', None) is None:
            validated_data['manage_by_id'] = None
        project: Project = super().create(validated_data)
        self.__set_active_version(project=project, active_version=set_active_version)
        self.__set_project_statuses(project=project, statuses=statuses_map)
        return project

    def update(self, instance, validated_data):
        set_active_version = validated_data.pop('set_active_version', None)
        statuses_map = validated_data.pop('statuses_map', None)
        if validated_data.get('category_id', None) is None and validated_data.get('category', None) is None:
            validated_data['category_id'] = None
        if validated_data.get('type_id', None) is None and validated_data.get('type', None) is None:
            validated_data['type_id'] = None
        if validated_data.get('manage_by_id', None) is None and validated_data.get('manage_by', None) is None:
            validated_data['manage_by_id'] = None
        project: Project = super().update(instance, validated_data)
        self.__set_active_version(project=project, active_version=set_active_version)
        self.__set_project_statuses(project=project, statuses=statuses_map)
        return project

    def __set_active_version(self, project: Project, active_version: Optional[Dict]) -> None:
        try:
            if active_version:
                active_version_obj = ProjectVersion.objects.filter(id=active_version.get('id', None)).first()
                if active_version_obj is None:
                    active_version_obj = ProjectVersion.objects.create(**active_version)
                active_version_obj.in_work = True
                active_version_obj.save()
            else:
                project.project_versions.update(in_work=False)
        except Exception as _e:
            raise serializers.ValidationError({'error': _e})

    def __set_project_statuses(self, project: Project, statuses: Optional[Dict]) -> None:
        try:
            if statuses and len(statuses) > 0:
                project_statuses_ids = set(project.project_statuses.all().values_list('status_id', flat=True))
                included_statuses_ids = set([s.get('id', None) for s in statuses if s.get('id', None) is not None])
                to_create = included_statuses_ids - project_statuses_ids
                if len(to_create) > 0:
                    ProjectStatus.objects.bulk_create([
                        ProjectStatus(project=project, status_id=status_id) for status_id in to_create
                    ])
                to_delete = project_statuses_ids - included_statuses_ids
                if len(to_delete) > 0:
                    ProjectStatus.objects.filter(project=project, status_id__in=to_delete).delete()
            else:
                project.project_statuses.all().delete()
        except Exception:
            raise serializers.ValidationError({'error': 'Нельзя удалить статусы из проекта: есть прикрепленные задачи'})
