from rest_framework import serializers

from core.models import User
from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='tg_chat_id', read_only=True)
    username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'username', 'verification_code', 'user_id')


class BotVerifySerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6)

    class Meta:
        fields = ('verification_code', )

    def validate_verification_code(self, code: str) -> str:
        try:
            self._tg_user: TgUser = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise serializers.ValidationError('Validation code not found')

        return code

    def update(self, instance: User, validated_data: dict) -> TgUser:
        self._tg_user.user = instance
        self._tg_user.verification_code = None
        self._tg_user.save(update_fields=('user', 'verification_code'))
        return self._tg_user

    def to_representation(self, instance):
        return TgUserSerializer(self._tg_user).data
