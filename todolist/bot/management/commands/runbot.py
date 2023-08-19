import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from typing import Protocol

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse, Update, Message, CallbackQuery
from goals.models import Goal, GoalCategory

logger = logging.getLogger(__name__)


class Handler(Protocol):
    """
    Protocol for a callable handler
    """
    def __call__(self, tg_user: TgUser, msg: Message = ..., cb_data: str = ...) -> None:
        ...


class Command(BaseCommand):
    help = 'Run telegram bot'
    create_goal_data: dict = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client: TgClient = TgClient()

    def get_handler(self, command: str) -> Handler | None:
        """
        Return a callable method based on the given command
        """
        commands = {
            '/goals': self.handle_goals,
            '/create': self.handle_create,
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
                if item.message:
                    self.handle_message(item.message)
                elif item.callback_query:
                    self.handle_callback(item.callback_query)

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

    def handle_callback(self, cb_query: CallbackQuery):
        tg_user: TgUser = TgUser.objects.get(tg_chat_id=cb_query.message.chat.id)
        msg = cb_query.message
        cb_data = cb_query.data
        self.handle_create(tg_user, msg, cb_data=cb_data)

    def handle_unauthorized(self, tg_user: TgUser) -> None:
        """
        Handle an unauthorized user
        """
        tg_user.update_verification_code()
        unauthorized_msg = f'Please enter this verification code on {settings.SITE_URL}: {tg_user.verification_code}'
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unauthorized_msg)

    def handle_authorized(self, tg_user: TgUser, msg: Message) -> None:
        """
        Handle message from an authorized user
        """
        command_handler = self.get_handler(msg.text)

        # If message text is one of supported commands
        if command_handler:
            command_handler(tg_user, msg)
        # If message text is expected to contain data for handle_create method
        elif tg_user.tg_chat_id in self.create_goal_data:
            self.handle_create(tg_user, msg)
        else:
            unknown_command_msg = 'Unknown command'
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unknown_command_msg)

    def handle_goals(self, tg_user: TgUser, msg: Message = None) -> None:
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

    def handle_create(self, tg_user: TgUser, msg: Message = None, cb_data: str = None):
        chat_id: int = tg_user.tg_chat_id
        user_goal_data = self.create_goal_data.get(chat_id)

        # Step 1: creation hasn't been started yet
        if user_goal_data is None:
            # Get existing categories' titles
            category_titles = (
                GoalCategory.objects.filter(user_id=tg_user.user_id)
                .exclude(is_deleted=True)
                .values_list('title', flat=True)
            )
            if not category_titles:
                no_categories_message = 'No categories found. Please use /createcat command to create a category'
                self.tg_client.send_message(chat_id=chat_id, text=no_categories_message)
                return

            # Send a message with category titles as buttons
            choose_category_msg = 'Please choose a category from the following:\n'
            buttons = [{'text': title, 'callback_data': title} for title in category_titles]
            buttons.append({'text': 'Cancel goal creation', 'callback_data': '/cancel'})
            markup = {'inline_keyboard': [buttons]}
            self.tg_client.send_message(chat_id=chat_id, text=choose_category_msg, reply_markup=markup)

            # Store user's chat id for the following steps
            self.create_goal_data[chat_id] = {}

        # Step 2: creation started, expecting category title
        elif cb_data:
            if cb_data == '/cancel':
                del self.create_goal_data[chat_id]
                self.tg_client.send_message(chat_id, text='Goal creation cancelled')
            elif not user_goal_data.get('category'):
                user_goal_data['category'] = cb_data
                self.tg_client.send_message(chat_id, text='Please enter goal title:')

        # Step 3: category title was saved, expecting goal title
        elif category_title := user_goal_data.get('category'):
            goal_title = msg.text
            try:
                category = GoalCategory.objects.exclude(is_deleted=True).get(title=category_title)
            except GoalCategory.DoesNotExist:
                # If category was deleted before user finished creation
                del self.create_goal_data[chat_id]
                self.tg_client.send_message(chat_id, text='Something went wrong, please start over')
                return

            goal = Goal.objects.create(title=goal_title, category_id=category.id, user_id=tg_user.user.id)
            goal_url = (
                    settings.SITE_URL +
                    f'/boards/{goal.category.board_id}/categories/{goal.category_id}/goals?goal={goal.id}'
            )
            markup = {'inline_keyboard': [[{'text': 'View goal', 'url': goal_url}]]}

            self.tg_client.send_message(chat_id, text='Goal successfully created', reply_markup=markup)
            del self.create_goal_data[chat_id]
        else:
            # Failsafe for if something goes wrong
            self.create_goal_data.pop(chat_id, None)
            self.tg_client.send_message(chat_id, text='Something went wrong, please start over')
