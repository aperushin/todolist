import logging
from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse, Update, Message

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run telegram bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options) -> None:
        offset = 0

        logger.info('Bot started')
        while True:
            response: GetUpdatesResponse = self.tg_client.get_updates(offset=offset)

            item: Update
            for item in response.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        tg_user: TgUser
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=msg.chat.id)

        if created:
            greeting_message = f'Hello there, your verification code: {tg_user.verification_code}'
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=greeting_message)
        elif not tg_user.user:
            self.handle_unauthorized(tg_user)
        else:
            self.handle_authorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser) -> None:
        tg_user.update_verification_code()
        unauthorized_message = f'Please enter this verification code on our website: {tg_user.verification_code}'
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unauthorized_message)

    def handle_authorized(self, tg_user: TgUser, msg: Message) -> None:
        # Echo
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=msg.text)
