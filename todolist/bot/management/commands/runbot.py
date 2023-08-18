import logging

from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from typing import Callable

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse, Update, Message
from goals.models import Goal

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run telegram bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client: TgClient = TgClient()

    def get_handler(self, command: str) -> Callable[[TgUser, Message], None] | None:
        """
        Return a callable method based on the given command
        """
        commands = {
            '/goals': self.handle_goals,
        }
        return commands.get(command)

    def handle(self, *args, **options) -> None:
        """
        Main loop
        """
        offset = 0

        logger.info('Bot started')
        while True:
            response: GetUpdatesResponse = self.tg_client.get_updates(offset=offset)

            item: Update
            for item in response.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        """
        Handle message from a user
        """
        tg_user: TgUser
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=msg.chat.id)

        if created:
            greeting_msg = f'Hello there, your verification code: {tg_user.verification_code}'
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=greeting_msg)
        elif not tg_user.user:
            self.handle_unauthorized(tg_user)
        else:
            self.handle_authorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser) -> None:
        """
        Handle an unauthorized user
        """
        tg_user.update_verification_code()
        unauthorized_msg = f'Please enter this verification code on our website: {tg_user.verification_code}'
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unauthorized_msg)

    def handle_authorized(self, tg_user: TgUser, msg: Message) -> None:
        """
        Handle message from an authorized user
        """
        command_handler = self.get_handler(msg.text)
        if command_handler:
            command_handler(tg_user, msg)
        else:
            unknown_command_msg = 'Unknown command'
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unknown_command_msg)

    def handle_goals(self, tg_user: TgUser, msg: Message) -> None:
        """
        Handle /goals command

        Sends a list of the user's goal titles to the user
        """
        goal_titles: QuerySet = (
            Goal.objects.filter(user_id=tg_user.user_id)
            .exclude(status=Goal.Status.archived)
            .values_list('title', flat=True)
        )

        if goal_titles:
            goals_reply_msg = 'Your currently active goals:\n' + '\n'.join(goal_titles)
        else:
            goals_reply_msg = "You don't have any active goals at the moment"

        self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=goals_reply_msg)
