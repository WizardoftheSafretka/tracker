from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'tg_chat_id')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'tg_chat_id': {'required': False, 'allow_blank': True}
        }