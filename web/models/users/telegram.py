import json
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, field_validator


class ChatTypeEnum(StrEnum):
    private: str = "private"
    group: str = "group"
    supergroup: str = "supergroup"
    channel: str = "channel"


class WebAppUser(BaseModel):
    id: int
    first_name: str
    is_bot: bool | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class WebAppChat(BaseModel):
    id: int
    type: ChatTypeEnum
    title: str | None = None
    username: str | None = None
    photo_url: str | None = None


class WebAppInitData(BaseModel):
    query_id: str | None = None
    user: WebAppUser | None = None
    receiver: WebAppUser | None = None
    chat: WebAppChat | None = None
    chat_type: ChatTypeEnum | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None
    auth_date: datetime
    hash: str

    # Если поле представлено моделью, то надо распарсить из JSON строки
    @field_validator("user", "receiver", "chat", mode="before")  # noqa
    @classmethod
    def parse_json(cls, value: str | None) -> dict[str, Any] | None:
        if value is None:
            return None
        return json.loads(value)

    @field_validator("auth_date", mode="before")  # noqa
    @classmethod
    def validate_auth_date(cls, value: str) -> datetime:
        """
        Конвертирует unix время в datetime по UTC без тайм зоны

        Args:
            value (int): unix время авторизации

        Returns:
            datetime
        """
        return datetime.fromtimestamp(int(value), UTC)
