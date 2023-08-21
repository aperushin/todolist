import logging
import marshmallow_dataclass
import requests
from enum import Enum

from django.conf import settings
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

logger: logging.Logger = logging.getLogger(__name__)

GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)


class BotMethod(str, Enum):
    """Telegram bot methods"""
    SEND_MESSAGE = 'sendMessage'
    GET_UPDATES = 'getUpdates'


class TgClient:
    """Telegram client

    Args:
        token (:obj:`str`, optional): Bot authorization token. If not provided, gets token from Django settings.

    """
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.TELEGRAM_BOT_TOKEN

    def get_url(self, method: BotMethod) -> str:
        """Get bot API url with the given method

        Args:
            method (BotMethod): Method from Enum class

        Returns:
            str: URL string

        """
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def _get(self, method: BotMethod, **params) -> dict:
        """Send GET request to the bot API with the given method and parameters

        Args:
            method (BotMethod): Method from Enum class
            params: Request parameters.

        Returns:
            Response data dictionary

        Raises:
            ValueError: If the response has a status other than 200

        """
        url: str = self.get_url(method=method)
        response: requests.Response = requests.get(url, json=params)
        if response.status_code != 200:
            logger.error(f'{response.status_code}: {response.json().get("description")}')
            raise ValueError('Invalid response')
        return response.json()

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Get bot updates

        Returns:
            GetUpdatesResponse: GetUpdatesResponse object with data from the response

        """
        response_data: dict = self._get(BotMethod.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponseSchema().load(response_data)

    def send_message(self, chat_id: int, text: str, reply_markup: dict = None) -> SendMessageResponse:
        """Send a message to a telegram chat with the given chat id

        Args:
            chat_id (int): Telegram chat id
            text (str): Message text
            reply_markup (:obj:`dict`, optional): Reply markup dictionary

        Returns:
            SendMessageResponse: SendMessageResponse object with data from the response

        """
        params: dict = dict(method=BotMethod.SEND_MESSAGE, chat_id=chat_id, text=text)
        if reply_markup:
            params['reply_markup'] = reply_markup

        response_data: dict = self._get(**params)
        return SendMessageResponseSchema().load(response_data)
