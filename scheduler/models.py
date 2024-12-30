from pydantic import BaseModel


class Grade(BaseModel):
    date: str | None
    grade: int
    weight: int


class NewGrade(BaseModel):
    subject: str
    grades: list[Grade]


class Period(BaseModel):
    name: str
    date_begin: str
    date_end: str
    grades: list[Grade] | str | None


class GradeFinal(BaseModel):
    subject: str
    periods: list[Period]
