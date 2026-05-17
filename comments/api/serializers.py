from typing import Dict

from rest_framework import serializers

from comments.models import WorkComment
from users.api.serializers import UserExtendedShortSerializer
from users.models import UserExtended
from work.models.work import Work


class WorkCommentSerializer(serializers.ModelSerializer):

    created_by = UserExtendedShortSerializer(many=False, read_only=True)
    work = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    parent = serializers.SlugRelatedField(read_only=True, slug_field='slug', required=False, allow_null=True)

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

    work_id = serializers.SlugRelatedField(
        queryset=Work.objects.all(),
        slug_field='slug',
        source='work',
        write_only=True,
        required=True,
        allow_null=False,
    )

    parent_id = serializers.SlugRelatedField(
        queryset=WorkComment.objects.all(),
        slug_field='slug',
        source='parent',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = WorkComment
        fields = [
            'id', 'description', 'slug', 'created', 'updated', 'created_by', 'work', 'parent',
            'created_by_id', 'work_id', 'parent_id',
        ]
        read_only_fields = ['slug', 'created', 'updated']

    def create(self, validated_data: Dict) -> WorkComment:
        comment: WorkComment = super().create(validated_data)
        return comment

    def update(self, instance: WorkComment, validated_data: Dict) -> WorkComment:
        comment: WorkComment = super().update(instance, validated_data)
        return comment
