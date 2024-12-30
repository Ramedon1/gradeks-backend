import asyncio
from collections import defaultdict

from pydantic import ValidationError

from db.manager import db_manager
from rediska import redis_manager
from web.models.users.user import (FinallyGrade, InfoFinallyGrade, NewGrade,
                                   ReferralInfo, SpecDiaryInfo)


async def get_distribution(user_id: str) -> bool:
    user_distribution = await db_manager.distribution.get_distribution_status_user(
        user_id
    )
    return user_distribution


async def get_new_grades(user_id: str) -> list[NewGrade]:
    raw_grades = await redis_manager.new_grades.get_all_new_grades(user_id)

    validated_grades = []
    if not raw_grades:
        return []
    for entry in raw_grades:
        try:
            validated_grade = NewGrade(
                grade=int(entry.get("new_grade")),
                old_grade=(
                    int(entry.get("old_grade")) if entry.get("old_grade") else None
                ),
                date=entry.get("grading_date") if entry.get("grading_date") else None,
                subject=entry.get("subject"),
                coff=int(entry.get("grade_weight")),
                is_final=entry.get("is_final") if entry.get("is_final") else None,
            )
            validated_grades.append(validated_grade)
        except ValidationError as e:
            print(f"Validation failed for entry: {entry} - {e}")

    return validated_grades


async def get_spec_diary_info(user_id: str) -> SpecDiaryInfo:
    spec_diary_info = await db_manager.users.get_spec_diary_info(user_id)
    return SpecDiaryInfo.model_validate(spec_diary_info, from_attributes=True)


async def get_referrals(user_id: str) -> list[ReferralInfo]:
    tg_id = await db_manager.users.get_telegram_id_by_user_id(user_id)
    referrals = await db_manager.referral.get_referrals(tg_id)
    return [
        ReferralInfo.model_validate(referral, from_attributes=True)
        for referral in referrals
    ]


async def get_special_referrals(user_id: str) -> list[ReferralInfo]:
    tg_id = await db_manager.users.get_telegram_id_by_user_id(user_id)
    referrals = await db_manager.referral.get_referrals(tg_id)
    validated_referrals = []

    if not referrals:
        return []

    for referral_data in referrals:
        referral = ReferralInfo.model_validate(referral_data, from_attributes=True)
        diary_linked = await db_manager.referral.get_diary_linked(referral.user_id)
        if not diary_linked:
            continue
        if diary_linked.linked_diary:
            validated_referrals.append(referral)

    return validated_referrals


async def get_final_grades(user_id: str):
    grades_user = await db_manager.grades_finally.get_finally_grades_by_user_id(user_id)

    grouped_grades = defaultdict(list)
    for grade in grades_user:
        grouped_grades[grade.quarter].append(
            InfoFinallyGrade(subject=grade.subject, grade=grade.grade)
        )

    final_grades_data = [
        {"quarter_name": quarter, "info_grades": grouped_grades[quarter]}
        for quarter in grouped_grades
    ]

    validated_final_grades = []
    for data in final_grades_data:
        validated_final_grade = FinallyGrade.model_validate(data, from_attributes=True)
        validated_final_grades.append(validated_final_grade)

    return validated_final_grades
