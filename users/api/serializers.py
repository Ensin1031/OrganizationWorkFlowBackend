from rest_framework import serializers

from users.models import UserExtended


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserExtended
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = UserExtended.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
