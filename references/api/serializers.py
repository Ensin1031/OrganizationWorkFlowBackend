from rest_framework import serializers

from references.models.status import StatusRow
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType

REFERENCE_FIELDS = ['id', 'name', 'description', 'slug', 'color', 'icon', 'created', 'updated', 'is_active']
REFERENCE_SHORT_FIELDS = ['id', 'name', 'slug', 'color', 'icon']


class ReferencesSerializerMixin(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)


class ReferencesShortSerializerMixin(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.CharField(read_only=True)


class StatusRowSerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = StatusRow
        fields = REFERENCE_FIELDS


class StatusRowShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = StatusRow
        fields = REFERENCE_SHORT_FIELDS


class WorkDifficultySerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = WorkDifficulty
        fields = REFERENCE_FIELDS


class WorkDifficultyShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = WorkDifficulty
        fields = REFERENCE_SHORT_FIELDS


class WorkPrioritySerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = WorkPriority
        fields = REFERENCE_FIELDS


class WorkPriorityShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = WorkPriority
        fields = REFERENCE_SHORT_FIELDS


class WorkTagSerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = WorkTag
        fields = REFERENCE_FIELDS


class WorkTagShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = WorkTag
        fields = REFERENCE_SHORT_FIELDS


class WorkTechnologySerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = WorkTechnology
        fields = REFERENCE_FIELDS


class WorkTechnologyShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = WorkTechnology
        fields = REFERENCE_SHORT_FIELDS


class WorkTypeSerializer(serializers.ModelSerializer, ReferencesSerializerMixin):
    class Meta:
        model = WorkType
        fields = REFERENCE_FIELDS


class WorkTypeShortSerializer(serializers.ModelSerializer, ReferencesShortSerializerMixin):
    class Meta:
        model = WorkType
        fields = REFERENCE_SHORT_FIELDS
