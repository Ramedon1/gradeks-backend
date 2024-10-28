from datetime import date

from pydantic import UUID4
from sqlalchemy import UUID
from sqlmodel import Field, SQLModel


class NewGrades(SQLModel, table=True):
    """
    Данные о новых оценках пользователя за день.

    Attributes:
        grade_id (UUID): внутренний идентификатор оценки
        user_id (UUID): внутренний идентификатор пользователя
        grading_date (date): дата выставление оценки в электронном дневнике
        subject (str): название предмета, по которому стоит оценка
        grade (int): оценка
        grade_old (int | None): старая оценка
        grade_weight (int): вес оценки, используется для расчета средней оценки
        long_name (str | None): полное название оценки
    """

    __tablename__ = "new_grades"

    grade_id: UUID4 = Field(foreign_key="grades.grade_id", primary_key=True)
    user_id: UUID4 = Field(foreign_key="users.user_id")
    grading_date: date = Field(default=None, nullable=True)
    subject: str = Field(default=None, nullable=True)
    grade: int = Field(default=None, nullable=True)
    grade_old: int = Field(default=None, nullable=True)
    grade_weight: int = Field(default=None, nullable=True)
    long_name: str | None = Field(default=None, nullable=True)
