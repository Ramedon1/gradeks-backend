from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.quarters import Quarters


class DbManagerQuarters(DbManagerBase):
    async def get_quarters(
        self, outer_session: AsyncSession | None = None
    ) -> Quarters | None:
        async with self.session_manager(outer_session) as session:
            result = await session.exec(select(Quarters))
            quarters = result.all()

            return quarters
