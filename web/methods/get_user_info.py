import asyncio

from db.manager import db_manager
from web.models.users.user import DistributionInfo, UserInfo


async def get_distribution(user_id: str) -> DistributionInfo:
    user_stats = await db_manager.distribution.get_distribution(user_id)
    return DistributionInfo.model_validate(user_stats, from_attributes=True)


async def get_diary_info(user_id: str) -> dict:
    diary_info = await db_manager.grades.get_diary_info(user_id)
    return diary_info
