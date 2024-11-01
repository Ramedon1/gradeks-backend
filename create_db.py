import asyncio
from datetime import date, timedelta
from importlib.metadata import distribution
from random import randint
from uuid import uuid4  # Correctly importing uuid4 from the uuid module

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from db.manager import db_manager
from db.models.grades import Grades
from db.models.new_grades import NewGrades
from db.models.quarters import Quarters
from db.models.users import User
from db.session import engine


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with db_manager.session() as session:
        # Create and add quarters
        quarters = [
            Quarters(
                quarter_name="Первая четверть",
                quarter_date_start=date(2024, 9, 1),
                quarter_date_end=date(2024, 10, 25),
            ),
            Quarters(
                quarter_name="Вторая четверть",
                quarter_date_start=date(2024, 11, 4),
                quarter_date_end=date(2024, 12, 29),
            ),
            Quarters(
                quarter_name="Третья четверть",
                quarter_date_start=date(2025, 1, 9),
                quarter_date_end=date(2025, 3, 25),
            ),
            Quarters(
                quarter_name="Четвертая четверть",
                quarter_date_start=date(2025, 4, 4),
                quarter_date_end=date(2025, 5, 29),
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

        # Create and add grades
        for _ in range(1, 10):
            grade = Grades(
                user_id=user.user_id,
                subject="Math",
                grade=randint(2, 5),
                grade_weight=randint(1, 6),
                grading_date=date(2024, 9, 1) + timedelta(days=randint(0, 120)),
            )
            session.add(grade)

            new_grade = NewGrades(
                grade_id=grade.grade_id,
                user_id=user.user_id,
                subject="Math",
                grade=randint(2, 5),
                grade_weight=randint(1, 6),
                grading_date=date(2024, 9, 1) + timedelta(days=randint(0, 120)),
            )
            session.add(new_grade)

        await session.commit()  # Commit all grades at once

    await db_manager.close()  # Ensure db_manager is closed properly


asyncio.run(main())
