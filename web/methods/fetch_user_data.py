import asyncio

from web.methods.get_user_info import (get_diary_info, get_distribution,
                                       get_grades_by_period, get_referrals)
from web.models.users.user import UserInfo


async def fetch_user_data(user_id, start_date, end_date):
    user_distributions_task = get_distribution(user_id)
    user_diary_info_task = get_diary_info(user_id)
    user_grades_task = get_grades_by_period(user_id, start_date, end_date)
    user_referrals_task = get_referrals(user_id)
    (
        user_distributions,
        user_diary_info,
        user_grades,
        user_referrals,
    ) = await asyncio.gather(  # noqa
        user_distributions_task,
        user_diary_info_task,
        user_grades_task,
        user_referrals_task,
    )

    return UserInfo.model_validate(
        {
            "distributions": user_distributions,
            "diary_info": user_diary_info,
            "grades": user_grades,
            "referrals": user_referrals,
        }
    )
