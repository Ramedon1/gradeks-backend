from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.distribution import Distribution


class DbManagerDistribution(DbManagerBase):
    async def get_distribution(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> Distribution | None:
        async with self.session_manager(outer_session) as session:
            statement = select(Distribution.distribution_status).where(
                Distribution.user_id == user_id
            )
            result = await session.exec(statement)
            distribution = result.one_or_none()

            return distribution

    async def get_distribution_users_active(
        self,
        user_id: str | UUID,
        distribution_type: str,
        outer_session: AsyncSession | None = None,
    ) -> list[Distribution]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Distribution)
                .where(Distribution.user_id == user_id)
                .where(Distribution.distribution_type == distribution_type)
                .where(Distribution.distribution_status == True)
            )
            result = await session.exec(statement)
            distribution = result.all()

            return distribution

    async def edit_distribution(
        self,
        user_id: str | UUID,
        distribution_type: str,
        outer_session: AsyncSession | None = None,
    ) -> Distribution:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Distribution)
                .where(Distribution.user_id == user_id)
                .where(Distribution.distribution_type == distribution_type)
            )
            result = await session.exec(statement)
            distribution = result.one_or_none()
            distribution.distribution_status = True
            await session.commit()
            await session.refresh(distribution)

            return distribution
