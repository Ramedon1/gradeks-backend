from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.referral import Referral, ReferralCheckListDiary


class DbManagerReferrals(DbManagerBase):
    async def set_referral(
        self,
        user_id: str | UUID,
        invited_by: int | None,
        outer_session: AsyncSession | None = None,
    ) -> Referral:
        async with self.session_manager(outer_session) as session:
            referral = Referral(user_id=user_id, invited_by=invited_by)
            session.add(referral)

            await session.commit()
            await session.refresh(referral)

            return referral

    async def get_referral_invited(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> Referral:
        async with self.session_manager(outer_session) as session:
            statement = select(Referral).where(Referral.user_id == user_id)
            result = await session.exec(statement)
            referral = result.one_or_none()

            return referral

    async def get_referrals(
        self, invited_by: int, outer_session: AsyncSession | None = None
    ) -> list[Referral] | None:
        async with self.session_manager(outer_session) as session:
            statement = select(Referral).where(Referral.invited_by == invited_by)
            result = await session.exec(statement)
            referrals = result.all()

            return referrals

    async def set_diary_linked(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> ReferralCheckListDiary:
        async with self.session_manager(outer_session) as session:
            referral = ReferralCheckListDiary(user_id=user_id, linked_diary=True)
            session.add(referral)

            await session.commit()
            await session.refresh(referral)

            return referral

    async def get_diary_linked(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> ReferralCheckListDiary | None:
        async with self.session_manager(outer_session) as session:
            statement = select(ReferralCheckListDiary).where(
                ReferralCheckListDiary.user_id == user_id
            )
            result = await session.exec(statement)
            referral = result.one_or_none()

            return referral
