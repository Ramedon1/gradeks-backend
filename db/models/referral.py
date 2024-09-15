import uuid

from sqlmodel import Field, SQLModel
from db.models.users import User


class Referral(SQLModel, table=True):
    """
    Список пользователей, которые пригласили других пользователей

    Attributes:
        user_id (int): идентификатор пользователя в системе
        invited_by (int | None): идентификатор пользователя, которого пригласили, или он не приглашен
    """

    __tablename__ = "referrals"

    user_id: int = Field(foreign_key=User.user_id, primary_key=True)
    invited_by: int | None = Field(default_factory=uuid.uuid4)
