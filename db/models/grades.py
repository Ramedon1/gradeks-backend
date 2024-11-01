import uuid
from datetime import date

from pydantic import UUID4
from sqlalchemy import UUID
from sqlmodel import Field, SQLModel


class Grades(SQLModel, table=True):
    """
    Данные о оценках пользователя.

    Attributes:
        grade_id (UUID): внутренний идентификатор оценки
        user_id (UUID): внутренний идентификатор пользователя
        grading_date (date): дата выставление оценки в электронном дневнике
        subject (str): название предмета, по которому стоит оценка
        grade (int): оценка
        grade_weight (int): вес оценки, используется для расчета средней оценки
    """

    __tablename__ = "grades"

    grade_id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID4 = Field(foreign_key="users.user_id")
    grading_date: date = Field(default=None, nullable=True)
    subject: str = Field(default=None, nullable=True)
    grade: int = Field(default=None, nullable=True)
    grade_weight: int = Field(default=None, nullable=True)
