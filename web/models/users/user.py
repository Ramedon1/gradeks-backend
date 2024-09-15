from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GradesInfo(BaseModel):
    grading_date: datetime
    subject: str
    grade: int
    grade_weight: int
    long_name: str | None


class ReferralInfo(BaseModel):
    user_id: UUID
    invited_by: str


class DiaryInfo(BaseModel):
    diary_id: str
    diary_link: bool


class DistributionInfo(BaseModel):
    distribution_type: str | None
    distribution_status: bool | None


class UserInfo(BaseModel):
    diary: DiaryInfo | None = None
    grades: list[GradesInfo] | None = None
    distribution: list[DistributionInfo] | None = None
    referrals: list[ReferralInfo] | None = None
    is_active: bool = True

    # TODO: В будущем сделать итоговые оценки

    model_config = ConfigDict(from_attributes=True)
