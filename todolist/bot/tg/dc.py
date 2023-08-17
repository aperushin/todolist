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
class Update:
    update_id: int
    message: Message

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
