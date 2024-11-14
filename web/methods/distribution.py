from uuid import UUID

from db.manager import db_manager
from web.models.users.user import Distribution


async def activate_distribution(user_id: str | UUID) -> Distribution:
    await db_manager.distribution.activate_distribution(user_id)
    return Distribution(distribution=True)


async def deactivate_distribution(user_id: str | UUID) -> Distribution:
    await db_manager.distribution.deactivate_distribution(user_id)
    return Distribution(distribution=True)
