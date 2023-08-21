from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.serializers import BaseSerializer

from bot.models import TgUser
from bot.tg.client import TgClient
from core.models import User
from bot.serializers import BotVerifySerializer


class BotVerifyView(UpdateAPIView):
    serializer_class: BaseSerializer = BotVerifySerializer
    permission_classes: BasePermission = (IsAuthenticated, )

    def get_object(self) -> User:
        return self.request.user

    def perform_update(self, serializer: BotVerifySerializer):
        tg_user: TgUser = serializer.save()
        verify_success_msg = 'Congratulations! You have successfully linked your telegram account'
        TgClient().send_message(chat_id=tg_user.chat_id, text=verify_success_msg)
