from pydantic import ValidationError

from db.manager import db_manager
from rediska import redis_manager
from web.models.users.user import NewGrade, ReferralInfo, SpecDiaryInfo


async def get_distribution(user_id: str) -> bool:
    user_distribution = await db_manager.distribution.get_distribution_status_user(
        user_id
    )
    return user_distribution


async def get_new_grades(user_id: str) -> list[NewGrade]:
    raw_grades = await redis_manager.new_grades.get_all_new_grades(user_id)

    validated_grades = []
    for entry in raw_grades:
        try:
            validated_grade = NewGrade(
                grade=int(entry.get("new_grade")),
                old_grade=(
                    int(entry.get("old_grade")) if entry.get("old_grade") else None
                ),
                date=entry.get("grading_date"),
                subject=entry.get("subject"),
                coff=int(entry.get("grade_weight")),
            )
            validated_grades.append(validated_grade)
        except ValidationError as e:
            print(f"Validation failed for entry: {entry} - {e}")

    return validated_grades


async def get_spec_diary_info(user_id: str) -> SpecDiaryInfo:
    spec_diary_info = await db_manager.users.get_spec_diary_info(user_id)
    return SpecDiaryInfo.model_validate(spec_diary_info, from_attributes=True)


async def get_referrals(user_id: str) -> list[ReferralInfo]:
    referrals = await db_manager.referral.get_referral(user_id)
    return [
        ReferralInfo.model_validate(referral, from_attributes=True)
        for referral in referrals
    ]
