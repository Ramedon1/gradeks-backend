import uuid

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class GradesFinally(SQLModel, table=True):

    __tablename__ = "grades_finally"

    grade_finally_id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID4 = Field(foreign_key="users.user_id")
    quarter: str = Field(default=None, nullable=True)
    subject: str = Field(default=None, nullable=True)
    grade: int = Field(default=None, nullable=True)
