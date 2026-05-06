from typing import List, Dict

from django.conf import settings
from rest_framework import serializers

from sprint.models import Sprint
from utils.choices.default_work_types_choices import DefaultWorkTypes


class SprintShortSerializer(serializers.ModelSerializer):

    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Sprint
        fields = [
            'id', 'name', 'slug', 'color', 'start_date', 'end_date', 'in_work', 'is_completed',
        ]


class SprintSerializer(serializers.ModelSerializer):
    """ Сериализатор для спринта """

    slug = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    works_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sprint
        fields = [
            'id', 'name', 'description', 'slug', 'color',
            'start_date', 'end_date', 'created', 'updated', 'in_work', 'is_completed', 'works_ids',
        ]
        read_only_fields = ['slug', 'created', 'updated']

    def get_works_ids(self, sprint: Sprint) -> List[int]:
        return list(sprint.works.exclude(
            type_id__in=[DefaultWorkTypes.EPIC.value, DefaultWorkTypes.STORY.value],
        ).filter(
            is_active=True,
        ).values_list('id', flat=True))

    def create(self, validated_data: Dict) -> Sprint:
        sprint: Sprint = super().create(validated_data)
        return sprint

    def update(self, instance: Sprint, validated_data: Dict) -> Sprint:
        sprint: Sprint = super().update(instance, validated_data)
        return sprint


class SprintUserLoadSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=True)
    user_email = serializers.EmailField(allow_null=True)
    user_photo = serializers.SerializerMethodField()
    user_full_name = serializers.CharField()
    user_lead_time = serializers.DurationField(allow_null=True)

    def get_user_photo(self, obj):
        request = self.context.get('request')
        user_photo = obj.get('user_photo')
        if not user_photo:
            return None
        media_url = settings.MEDIA_URL.rstrip('/')
        relative_path = f'{media_url}/{user_photo.lstrip("/")}'
        if request:
            return request.build_absolute_uri(relative_path)
        return relative_path


class SprintWithoutUsersLeadTimeSerializer(serializers.Serializer):
    total_lead_time = serializers.DurationField(allow_null=True)
