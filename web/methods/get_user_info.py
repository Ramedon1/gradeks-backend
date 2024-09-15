import asyncio
from datetime import datetime

from db.manager import db_manager
from web.models.users.user import (DiaryInfo, DistributionInfo, GradesInfo,
                                   ReferralInfo)


async def get_distribution(user_id: str) -> DistributionInfo:
    user_stats = await db_manager.distribution.get_distributions_user(user_id)
    return DistributionInfo.model_validate(user_stats, from_attributes=True)


async def get_diary_info(user_id: str) -> DiaryInfo:
    diary_info = await db_manager.users.get_diary_info(user_id)
    return DiaryInfo.model_validate(diary_info, from_attributes=True)


async def get_grades_by_period(
    user_id: str, start_date: datetime, end_date: datetime
) -> list[GradesInfo]:
    grades = await db_manager.grades.get_grades_by_period(user_id, start_date, end_date)
    return [GradesInfo.model_validate(grade, from_attributes=True) for grade in grades]


async def get_referrals(user_id: str) -> list[ReferralInfo]:
    referrals = await db_manager.referral.get_referral(user_id)
    return [
        ReferralInfo.model_validate(referral, from_attributes=True)
        for referral in referrals
    ]
