from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID
from sqlalchemy.testing.suite.test_reflection import users
from sqlmodel import Field, SQLModel


class Users_grades(SQLModel, table=True):
    """
    Данные о оценках пользователя.

    Attributes:
        user_id (UUID): внутренний идентификатор пользователя
        grading_date (datetime): дата выставление оценки в электронном дневнике
        subject (str): название предмета, по которому стоит оценка
        grade (int): оценка
        grade_wight (int): вес оценки, используется для расчета средней оценки
        long_name (str | None): полное название оценки
    """

    __tablename__ = "users_grades"

    user_id: UUID4 = Field(foreign_key=users.user_id, primary_key=True)
    grading_date: datetime = Field(default=None, nullable=True)
    subject: str = Field(default=None, nullable=True)
    grade: int = Field(default=None, nullable=True)
    grade_wight = int = Field(default=None, nullable=True)
    long_name: str | None = Field(default=None, nullable=True)
