from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.referral import Referral


class DbManagerReferrals(DbManagerBase):
    async def set_referral(self, user_id: int, invited_by: int | None,
                           outer_session: AsyncSession | None = None) -> Referral:
        async with self.session_manager(outer_session) as session:
            referral = Referral(user_id=user_id, invited_by=invited_by)
            session.add(referral)

            await session.commit()
            await session.refresh(referral)

            return referral
