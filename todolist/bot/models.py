import random
import string

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User

ALPHANUM: str = string.ascii_uppercase + string.ascii_lowercase + string.digits


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name=_('Telegram chat id'), unique=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, null=True)
    verification_code = models.CharField(max_length=6, null=True)

    @staticmethod
    def _generate_verification_code() -> str:
        code_length = 6
        code = ''.join([random.choice(ALPHANUM) for _ in range(code_length)])
        return code

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=('verification_code', ))

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.verification_code = self._generate_verification_code()
        return super(TgUser, self).save(*args, **kwargs)
