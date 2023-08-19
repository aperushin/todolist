from dataclasses import dataclass
from marshmallow import EXCLUDE


@dataclass
class Chat:
    id: int

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    chat: Chat
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class CallbackQuery:
    message: Message
    data: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    update_id: int
    message: Message | None = None
    callback_query: CallbackQuery | None = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: list[Update]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
