import os
from typing import Dict, Union, Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import UserExtended


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_photo_remove = serializers.BooleanField(write_only=True, required=False)
    profile_photo_init = serializers.FileField(write_only=True, required=False)
    full_name = serializers.CharField(read_only=True, source='get_full_name')

    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = UserExtended
        fields = [
            'id', 'username', 'email', 'password', 'profile_photo', 'profile_photo_remove', 'profile_photo_init',
            'first_name', 'last_name', 'second_name', 'full_name', 'birth_date',
        ]

    def get_profile_photo(self, obj):
        request = self.context.get('request')
        if obj.profile_photo:
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None

    def create(self, validated_data):
        user = UserExtended.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

    def update(self, instance: UserExtended, validated_data):
        profile_photo_remove = validated_data.get('profile_photo_remove', False)
        if profile_photo_remove:
            if instance.profile_photo:
                if os.path.isfile(instance.profile_photo.path):
                    os.remove(instance.profile_photo.path)
                instance.profile_photo = None
        profile_photo_init: Optional[InMemoryUploadedFile] = validated_data.get('profile_photo_init', None)
        if profile_photo_init is not None:
            if instance.profile_photo and os.path.isfile(instance.profile_photo.path):
                os.remove(instance.profile_photo.path)
            instance.profile_photo = profile_photo_init
        return super().update(instance, validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data: Dict[str, Union[str, Dict]] = super().validate(attrs)
        data['user'] = dict(UserSerializer(self.user, context={'request': self.context.get('request') or None}).data)
        return data
