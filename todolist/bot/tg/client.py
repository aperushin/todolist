import marshmallow_dataclass
import requests
from enum import Enum

from django.conf import settings
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)


class BotMethod(str, Enum):
    """
    Telegram bot methods
    """
    SEND_MESSAGE = 'sendMessage'
    GET_UPDATES = 'getUpdates'


class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.TELEGRAM_BOT_TOKEN

    def get_url(self, method: BotMethod) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def _get(self, method: BotMethod, **params) -> dict:
        url = self.get_url(method=method)
        response = requests.get(url, json=params)
        return response.json()

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response_data = self._get(BotMethod.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponseSchema().load(response_data)

    def send_message(self, chat_id: int, text: str, reply_markup: dict = None) -> SendMessageResponse:
        params: dict = dict(method=BotMethod.SEND_MESSAGE, chat_id=chat_id, text=text)
        if reply_markup:
            params['reply_markup'] = reply_markup

        response_data = self._get(**params)
        print(response_data)
        return SendMessageResponseSchema().load(response_data)
