import asyncio

from web.methods.get_user_info import (
    get_user_buffs,
    get_user_leagues,
    get_user_missions,
    get_user_ref_level_program,
    get_user_referrals,
    get_user_stats,
    get_user_ultimates,
    get_global_stat,
    get_buff_prices,
)
from web.models.users.user import UserInfo


async def fetch_user_data(user_id):
    referrals_task = get_user_referrals(user_id)
    stats_task = get_user_stats(user_id)
    buffs_task = get_user_buffs(user_id)
    ultimates_task = get_user_ultimates(user_id)
    missions_task = get_user_missions(user_id)
    ref_level_program_task = get_user_ref_level_program(user_id)
    leagues_task = get_user_leagues(user_id)
    global_stat_task = get_global_stat()
    buff_prices_task = get_buff_prices()
    (
        referrals,
        stats,
        buffs,
        ultimates,
        missions,
        ref_level_program,
        leagues,
        global_stat,
        buff_prices,
    ) = await asyncio.gather(  # noqa
        referrals_task,
        stats_task,
        buffs_task,
        ultimates_task,
        missions_task,
        ref_level_program_task,
        leagues_task,
        global_stat_task,
        buff_prices_task,
    )

    return UserInfo.model_validate(
        {
            "referrals": referrals,
            "stats": stats,
            "buffs": buffs,
            "ultimates": ultimates,
            "user_missions": missions,
            "user_ref_level_program": ref_level_program,
            "leagues": leagues,
            "global_stat": global_stat,
            "buff_prices": buff_prices,
        }
    )
