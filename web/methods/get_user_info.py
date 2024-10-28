from db.manager import db_manager
from web.models.users.user import NewGrade, ReferralInfo, SpecDiaryInfo


async def get_distribution(user_id: str) -> bool:
    user_distribution = await db_manager.distribution.get_distribution_status_user(
        user_id
    )
    return user_distribution


async def get_new_grades(user_id: str) -> list[NewGrade]:
    new_grades = await db_manager.new_grades.get_new_grades_by_user(user_id)
    return [NewGrade.model_validate(item, from_attributes=True) for item in new_grades]


async def get_spec_diary_info(user_id: str) -> SpecDiaryInfo:
    spec_diary_info = await db_manager.users.get_spec_diary_info(user_id)
    return SpecDiaryInfo.model_validate(spec_diary_info, from_attributes=True)


async def get_referrals(user_id: str) -> list[ReferralInfo]:
    referrals = await db_manager.referral.get_referral(user_id)
    return [
        ReferralInfo.model_validate(referral, from_attributes=True)
        for referral in referrals
    ]
