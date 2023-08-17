from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.serializers import BaseSerializer

from core.models import User
from bot.serializers import BotVerifySerializer


class BotVerifyView(UpdateAPIView):
    serializer_class: BaseSerializer = BotVerifySerializer
    permission_classes: BasePermission = (IsAuthenticated, )

    def get_object(self) -> User:
        return self.request.user
