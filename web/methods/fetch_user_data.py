import asyncio

from web.methods.get_diary_info import get_diary_info
from web.methods.get_user_info import (
    get_distribution,
    get_final_grades,
    get_new_grades,
    get_spec_diary_info,
    get_special_referrals,
)
from web.models.users.user import UserInfo


async def fetch_user_data(user_id: str, period_name: str) -> UserInfo:
    user_distribution_task = get_distribution(user_id)
    user_spec_diary_info_task = get_spec_diary_info(user_id)
    user_get_diary_info_task = get_diary_info(user_id, period_name)
    user_get_new_grades_task = get_new_grades(user_id)
    user_get_referrals_task = get_special_referrals(user_id)
    user_get_final_grades_task = get_final_grades(user_id)

    (
        user_distribution,
        user_spec_diary_info,
        user_diary_info,
        user_get_new_grades,
        user_get_referrals,
        user_get_final_grades,
    ) = await asyncio.gather(  # noqa
        user_distribution_task,
        user_spec_diary_info_task,
        user_get_diary_info_task,
        user_get_new_grades_task,
        user_get_referrals_task,
        user_get_final_grades_task,
    )

    return UserInfo.model_validate(
        {
            "distribution": user_distribution,
            "spec_diary": user_spec_diary_info,
            "diary_info": user_diary_info,
            "new_grades": user_get_new_grades,
            "referrals": user_get_referrals,
            "final_grades": user_get_final_grades,
        }
    )
