from pydantic import UUID4
from sqlalchemy import UUID
from sqlmodel import Field, SQLModel



class Distribution(SQLModel, table=True):
    """
    Данные о рассылке пользователям

    Attributes:
        user_id (UUID): внутренний идентификатор пользователя
        distribution_type (str | None): тип рассылки
        distribution_status (bool | None): статус рассылки
    """

    __tablename__ = "distributions"

    user_id: UUID4 = Field(foreign_key="users.user_id", primary_key=True)
    distribution_type: str | None = Field(nullable=True, default=None, max_length=255)
    distribution_status: bool | None = Field(nullable=True, default=True)
