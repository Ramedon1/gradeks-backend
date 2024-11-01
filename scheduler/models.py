from pydantic import BaseModel


class Grade(BaseModel):
    date: str
    grade: int
    weight: int


class NewGrade(BaseModel):
    subject: str
    grades: list[Grade]


class GradeSnapshot(BaseModel):
    user_id: str
    subject: str
    grading_date: str
    grades: list
    total_grade: int
    total_weight: int
