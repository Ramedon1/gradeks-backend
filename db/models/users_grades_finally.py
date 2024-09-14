from pydantic import UUID4
from sqlalchemy import UUID
from sqlalchemy.testing.suite.test_reflection import users
from sqlmodel import Field, SQLModel


class Users_grades_finally(SQLModel, table=True):
    """
    Данные о оценках пользователя.

    Attributes:
        user_id (UUID): внутренний идентификатор пользователя
        quarter (str): название четверти, по которому стоит оценка
        subject (str): название предмета, по которому стоит оценка
        grade (int): оценка
    """

    __tablename__ = "users_grades_finally"

    user_id: UUID4 = Field(foreign_key=users.user_id, primary_key=True)
    quarter: str = Field(default=None, nullable=True)
    subject: str = Field(default=None, nullable=True)
    grade: int = Field(default=None, nullable=True)
