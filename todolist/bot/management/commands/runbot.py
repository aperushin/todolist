import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet
from typing import Protocol

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import GetUpdatesResponse, Update, Message, CallbackQuery
from goals.models import Goal, GoalCategory, Board, BoardParticipant

logger = logging.getLogger(__name__)


class Handler(Protocol):
    """
    Protocol for a callable handler
    """
    def __call__(self, tg_user: TgUser, msg: Message = ..., cb_data: str = ...) -> None:
        ...


class Command(BaseCommand):
    help = 'Run telegram bot'

    # {tg_chat_id: {'command': '/command', 'data': 'data'}}
    create_data: dict = dict()

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
            '/creategoal': self.handle_create_goal,
            '/createcat': self.handle_create_cat,
            '/createboard': self.handle_create_board,
            '/cancel': self.handle_cancel,
        }
        return commands.get(command)

    def clear_creation_data(self, chat_id: int, send_error_msg: bool = False) -> None:
        """
        Remove the user's data from self.create_data

        :param send_error_msg: Send an error message to the user
        """
        self.create_data.pop(chat_id, None)
        if send_error_msg:
            self.tg_client.send_message(chat_id, text='Something went wrong, please start over')

    @staticmethod
    def generate_buttons_markup(button_names: list[str]) -> dict:
        """
        Generate buttons for telegram bot markup with button names as callback data

        Adds a /cancel command button to the end
        """
        buttons = [[{'text': name, 'callback_data': name}] for name in button_names]
        buttons.append([{'text': '[Cancel]', 'callback_data': '/cancel'}])
        return {'inline_keyboard': buttons}

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
        """
        Handle callback from a user's chat
        """
        tg_user: TgUser = TgUser.objects.get(tg_chat_id=cb_query.message.chat.id)
        msg = cb_query.message

        # Try parsing callback data as a command
        command_handler = self.get_handler(cb_query.data)
        if command_handler:
            command_handler(tg_user, msg=msg)
        else:
            # If not a command, should be data for create methods
            cb_data = cb_query.data
            self.handle_create(tg_user, cb_data=cb_data)

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
        # If message text is expected to contain data for create methods
        elif tg_user.tg_chat_id in self.create_data:
            self.handle_create(tg_user, msg)
        else:
            unknown_command_msg = 'Unknown command'
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=unknown_command_msg)

    # Command handlers

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

    def handle_create(self, tg_user: TgUser, msg: Message = None, cb_data: str = None) -> None:
        """
        Handle /create command or data for one of the other creation commands
        """
        chat_id: int = tg_user.tg_chat_id
        create_data: dict = self.create_data.get(chat_id)

        if create_data:
            # Creation process was already started, relay data to the creation command
            command_handler = self.get_handler(create_data.get('command'))
            if not command_handler:
                self.clear_creation_data(chat_id, send_error_msg=True)
                return

            command_handler(tg_user, msg, cb_data)
        else:
            # Send user buttons with available creation commands
            buttons = [
                {'text': 'a goal', 'callback_data': '/creategoal'},
                {'text': 'a category', 'callback_data': '/createcat'},
                {'text': 'a board', 'callback_data': '/createboard'},
            ]
            markup = {'inline_keyboard': [buttons]}
            self.tg_client.send_message(chat_id=chat_id, text='What would you like to create?', reply_markup=markup)

    def handle_cancel(self, tg_user: TgUser, msg: Message) -> None:
        """
        Handle /cancel command

        Clear creation data for the user's chat id, send user a message
        """
        self.clear_creation_data(tg_user.tg_chat_id)
        self.tg_client.send_message(tg_user.tg_chat_id, text='Creation cancelled')

    def handle_create_goal(self, tg_user: TgUser, msg: Message = None, cb_data: str = None):
        """
        Handle /creategoal command
        """
        chat_id: int = tg_user.tg_chat_id
        create_data: dict = self.create_data.get(chat_id)

        # Step 1: creation hasn't been started yet
        if create_data is None:
            # Get existing categories' titles
            category_titles = (
                GoalCategory.objects.filter(user_id=tg_user.user_id)
                .exclude(is_deleted=True)
                .values_list('title', flat=True)
            )
            if not category_titles:
                no_categories_message = 'No categories found. Please create a category first'
                self.tg_client.send_message(chat_id=chat_id, text=no_categories_message)
                return

            # Send a message with category titles as buttons
            choose_category_msg = 'Please choose a category from the following:\n'
            markup = self.generate_buttons_markup(category_titles)
            self.tg_client.send_message(chat_id=chat_id, text=choose_category_msg, reply_markup=markup)

            # Store user's chat id and the command for the following steps
            self.create_data[chat_id] = dict(command='/creategoal')

        # Step 2: creation started, expecting category title
        elif cb_data:
            create_data['data'] = cb_data
            self.tg_client.send_message(chat_id, text='Please enter goal title:')

        # Step 3: category title was saved, expecting goal title
        elif category_title := create_data.get('data'):
            goal_title = msg.text
            try:
                category = GoalCategory.objects.exclude(is_deleted=True).get(title=category_title)
            except GoalCategory.DoesNotExist:
                # If category was deleted before user finished creation
                self.clear_creation_data(chat_id, send_error_msg=True)
                return

            goal = Goal.objects.create(title=goal_title, category_id=category.id, user_id=tg_user.user.id)
            goal_url = (
                    settings.SITE_URL +
                    f'/boards/{goal.category.board_id}/categories/{goal.category_id}/goals?goal={goal.id}'
            )
            markup = {'inline_keyboard': [[{'text': 'View goal', 'url': goal_url}]]}

            self.tg_client.send_message(chat_id, text='Goal successfully created', reply_markup=markup)
            self.clear_creation_data(chat_id)
        else:
            # Failsafe for if something goes wrong
            self.clear_creation_data(chat_id, send_error_msg=True)

    def handle_create_cat(self, tg_user: TgUser, msg: Message = None, cb_data: str = None):
        """
        Handle /createcat command
        """
        chat_id: int = tg_user.tg_chat_id
        create_data: dict = self.create_data.get(chat_id)

        # Step 1: creation hasn't been started yet
        if create_data is None:
            # Get existing boards' titles
            board_titles = (
                Board.objects.filter(
                    participants__user=tg_user.user,
                    participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                    is_deleted=False
                ).values_list('title', flat=True)
            )
            if not board_titles:
                no_boards_message = 'No boards found. Please create a board first'
                self.tg_client.send_message(chat_id=chat_id, text=no_boards_message)
                return

            # Send a message with board titles as buttons
            choose_board_msg = 'Please choose a board from the following:\n'
            markup = self.generate_buttons_markup(board_titles)
            self.tg_client.send_message(chat_id=chat_id, text=choose_board_msg, reply_markup=markup)

            self.create_data[chat_id] = dict(command='/createcat')

        # Step 2: creation started, expecting board title
        elif cb_data:
            create_data['data'] = cb_data
            self.tg_client.send_message(chat_id, text='Please enter category title:')

        # Step 3: board title was saved, expecting category title
        elif board_title := create_data.get('data'):
            category_title = msg.text
            try:
                board = Board.objects.exclude(is_deleted=True).get(title=board_title)
            except Board.DoesNotExist:
                # If board was deleted before user finished creation
                self.clear_creation_data(chat_id, send_error_msg=True)
                return

            category = GoalCategory.objects.create(title=category_title, board_id=board.id, user_id=tg_user.user.id)
            category_url = (
                    settings.SITE_URL +
                    f'/boards/{category.board_id}/categories/{category.id}/goals'
            )
            markup = {'inline_keyboard': [[{'text': 'View category', 'url': category_url}]]}

            self.tg_client.send_message(chat_id, text='Category successfully created', reply_markup=markup)
            self.clear_creation_data(chat_id)
        else:
            # Failsafe for if something goes wrong
            self.clear_creation_data(chat_id, send_error_msg=True)

    def handle_create_board(self, tg_user: TgUser, msg: Message = None, cb_data: str = None):
        """
        Handle /createboard command
        """
        chat_id: int = tg_user.tg_chat_id
        create_data: dict = self.create_data.get(chat_id)

        # Step 1: creation hasn't been started yet
        if create_data is None:
            self.tg_client.send_message(chat_id, text='Please enter board title:')
            self.create_data[chat_id] = dict(command='/createboard')

        # Step 2: creation started, expecting board title
        else:
            board_title = msg.text
            with transaction.atomic():
                board = Board.objects.create(title=board_title)
                BoardParticipant.objects.create(board_id=board.id, user_id=tg_user.user.id)

            board_url = (
                    settings.SITE_URL +
                    f'/boards/{board.id}/goals'
            )
            markup = {'inline_keyboard': [[{'text': 'View board', 'url': board_url}]]}

            self.tg_client.send_message(chat_id, text='Board successfully created', reply_markup=markup)
            self.clear_creation_data(chat_id)
