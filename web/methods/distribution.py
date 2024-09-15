from uuid import UUID

from db.manager import db_manager
from web.models.users.user import DistributionInfo


async def activate_distribution(
    user_id: str | UUID, distribution_type: str
) -> DistributionInfo:
    distribution = await db_manager.distribution.activate_distribution(
        user_id, distribution_type
    )
    return DistributionInfo.model_validate(distribution, from_attributes=True)


async def deactivate_distribution(
    user_id: str | UUID, distribution_type: str
) -> DistributionInfo:
    distribution = await db_manager.distribution.deactivate_distribution(
        user_id, distribution_type
    )
    return DistributionInfo.model_validate(distribution, from_attributes=True)
