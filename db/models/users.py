import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID, BigInteger, Column
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
        diary_id (str): идентификатор пользователя в электронном дневнике
        diary_link (bool): подключен ли электронный дневник
        is_active (bool): активен ли пользователь
        grade_type (str): тип четвертных оценок, которые пользователь выбрал
    """

    __tablename__ = "users"

    user_id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    # Telegram Profile
    telegram_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    first_name: str | None = Field(nullable=True, default=None, max_length=255)
    last_name: str | None = Field(nullable=True, default=None, max_length=255)
    username: str | None = Field(nullable=True, default=None, max_length=255)
    created_at: datetime = CreatedAtField(index=True)
    diary_id: str | None = Field(default=None, nullable=True)
    diary_link: bool = Field(default=False, nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    grade_type: str = Field(default="new", nullable=False)
    # Telegram Auth
    telegram_hash: str = Field(nullable=False, default=None, max_length=255)


class UsersAvatar(SQLModel, table=True):
    """
    Аватарки пользователя

    Attributes:
        avatar_id (UUID): внутренний идентификатор аватарки
        user_id (UUID): внутренний идентификатор пользователя
        avatar (str): аватар ссылкой на тг аватар
    """

    __tablename__ = "users_avatar"

    avatar_id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID4 = Field(foreign_key="users.user_id", nullable=False)
    avatar: str = Field(nullable=False)
