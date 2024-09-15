import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class GradesInfo(BaseModel):
    grading_date: datetime
    subject: str
    grade: int
    grade_weight: int
    long_name: str | None


class ReferralInfo(BaseModel):
    invited_by: str


class DiaryInfo(BaseModel):
    diary_id: str
    diary_link: bool


class DistributionInfo(BaseModel):
    distribution_type: str | None
    distribution_status: bool | None


class UserInfo(BaseModel):
    user_id: int
    diary: DiaryInfo | None = None
    grades: list[GradesInfo] | None = None
    distribution: list[DistributionInfo] | None = None
    referrals: list[ReferralInfo] | None = None
    is_active: bool = True

    # TODO: В будущем сделать итоговые оценки

    model_config = ConfigDict(from_attributes=True)
