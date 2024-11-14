import asyncio
from datetime import date

from sqlmodel import SQLModel

from db.manager import db_manager
from db.models.periods import Periods
from db.models.users import User
from db.session import engine


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with db_manager.session() as session:
        # Create and add quarters
        quarters = [
            Periods(
                period_type="quarter",
                period_name="Первая четверть",
                period_date_start=date(2024, 9, 1),
                period_date_end=date(2024, 10, 25),
            ),
            Periods(
                period_type="quarter",
                period_name="Вторая четверть",
                period_date_start=date(2024, 11, 4),
                period_date_end=date(2024, 12, 29),
            ),
            Periods(
                period_type="quarter",
                period_name="Третья четверть",
                period_date_start=date(2025, 1, 9),
                period_date_end=date(2025, 3, 25),
            ),
            Periods(
                period_type="quarter",
                period_name="Четвертая четверть",
                period_date_start=date(2025, 4, 4),
                period_date_end=date(2025, 5, 29),
            ),
            Periods(
                period_type="semester",
                period_name="Первое полугодие",
                period_date_start=date(2024, 9, 1),
                period_date_end=date(2024, 12, 29),
            ),
            Periods(
                period_type="semester",
                period_name="Второе полугодие",
                period_date_start=date(2025, 1, 9),
                period_date_end=date(2025, 5, 29),
            ),
        ]

        session.add_all(quarters)  # Use add_all to add multiple items
        await session.commit()

        for quarter in quarters:
            await session.refresh(quarter)

        # Insert the user and commit
        user = User(
            telegram_id=123123123,
            first_name="ASdd",
            last_name="dasd",
            username="asd",
            diary_link=True,
            diary_id="3863E2BB1436B44C04C5EC565CE59A19",
            telegram_hash="asd",
            is_active=True,
        )
        session.add(user)
        await session.commit()  # Commit user here
        await session.refresh(user)  # Refresh to ensure the user ID is available


    await db_manager.close()  # Ensure db_manager is closed properly


asyncio.run(main())
