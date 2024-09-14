import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID
from sqlmodel import Field, SQLModel

from common.common import CreatedAtField


class User(SQLModel, table=True):
    """
    Данные о самом пользователе: внутренний id и связь с данными в телеге.

    Attributes:
        user_id (UUID): внутренний идентификатор пользователя
        telegram_id (int): Telegram ID пользователя
        first_name (str | None): имя, если есть
        last_name (str | None): фамилия, если есть
        username (str | None): username в телеге, если есть
        telegram_hash (str | None): хэш для авторизации пользователя в телеге
        created_at (datetime): время создания пользователя
        diary_link (bool): подключен ли электронный дневник
    """

    __tablename__ = "users"

    user_id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    # Telegram Profile
    telegram_id: int = Field(nullable=False)
    first_name: str | None = Field(nullable=True, default=None, max_length=255)
    last_name: str | None = Field(nullable=True, default=None, max_length=255)
    username: str | None = Field(nullable=True, default=None, max_length=255)
    created_at: datetime = CreatedAtField(index=True)
    diary_link: bool = Field(default=False, nullable=False)
    # Telegram Auth
    telegram_hash: str = Field(nullable=False, default=None, max_length=255)
