from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GradesInfo(BaseModel):
    coff: int
    grade: int
    date: str


class SubjectsInfo(BaseModel):
    subject_name: str
    grades: list[GradesInfo] | None
    new_type_grade: float | None
    old_type_grade: float | None


class DiaryInfo(BaseModel):
    quarter_name: str
    quarter_date: str
    type_grade: str
    subjects: list[SubjectsInfo] | None


class ReferralInfo(BaseModel):
    user_id: UUID
    invited_by: str


class NewGrade(BaseModel):
    grade: int
    old_grade: int | None
    date: str
    subject: str
    coff: int


class GradeType(BaseModel):
    grade_type: str


class SpecDiaryInfo(BaseModel):
    diary_id: str | None
    diary_link: bool | None


class LinkDiary(BaseModel):
    spec_diary: SpecDiaryInfo | None
    diary_info: list[DiaryInfo] | None


class DiaryConnect(BaseModel):
    diary_id: str


class GradeTypeFilter(BaseModel):
    filter: str


class Distribution(BaseModel):
    distribution_status: bool | None


class UserInfo(BaseModel):
    spec_diary: SpecDiaryInfo | None = None
    diary_info: list[DiaryInfo] | None = None
    new_grades: list[NewGrade] | None = None
    distribution: bool | None = None
    referrals: list[ReferralInfo] | None = None
    is_active: bool = True

    # TODO: В будущем сделать итоговые оценки

    model_config = ConfigDict(from_attributes=True)
