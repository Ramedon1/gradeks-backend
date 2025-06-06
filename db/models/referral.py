import uuid

from pydantic import UUID4
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class Referral(SQLModel, table=True):
    """
    Список пользователей, которые пригласили других пользователей

    Attributes:
        user_id (UUID): идентификатор пользователя в системе (приглашенный, тот кого пригласили по ссылке)
        invited_by (int | None): идентификатор пользователя (пригласитель)
    """

    __tablename__ = "referrals"

    user_id: UUID4 = Field(foreign_key="users.user_id", primary_key=True)
    invited_by: int | None = Field(
        sa_column=Column(BigInteger, nullable=True)  # Explicitly use BigInteger here
    )


class ReferralCheckListDiary(SQLModel, table=True):
    """
    Список рефералов, которые подключили дневник

    Attributes:
        user_id (UUID): идентификатор пользователя в системе (приглашенный)
        linked_diary (bool): флаг подключения дневника
    """

    __tablename__ = "referral_check_list_diarys"

    user_id: UUID4 = Field(foreign_key="users.user_id", primary_key=True)
    linked_diary: bool = Field(default=False)
