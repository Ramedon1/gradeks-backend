from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.periods import Periods


class DbManagerPeriods(DbManagerBase):
    async def get_periods_by_name(
        self, period_name: str, outer_session: AsyncSession | None = None
    ) -> list[Periods]:
        async with self.session_manager(outer_session) as session:
            result = await session.exec(
                select(Periods).where(Periods.period_type == period_name)
            )
            periods = result.all()

            return periods
