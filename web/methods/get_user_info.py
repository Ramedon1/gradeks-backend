import asyncio


from db.manager import db_manager
from web.models.users.user import (
    UserInfo, DistributionInfo
)



async def get_user_distribution(user_id: str) -> DistributionInfo:

    user_stats = await db_manager.distribution.get_distribution(user_id)
    return StatsInfo.model_validate(user_stats, from_attributes=True)
