from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name=_('Telegram chat id'), unique=True, primary_key=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, null=True)
    verification_code = models.CharField(max_length=settings.VERIFICATION_CODE_LENGTH, null=True)

    @staticmethod
    def _generate_verification_code() -> str:
        return get_random_string(settings.VERIFICATION_CODE_LENGTH)

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=('verification_code', ))

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.verification_code = self._generate_verification_code()
        return super(TgUser, self).save(*args, **kwargs)
