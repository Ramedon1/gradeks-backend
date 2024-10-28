import asyncio
from datetime import date, timedelta
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
        quarters = [
            Quarters(
                quarter_name="Первая четверть",
                quarter_date_start=date(2024, 9, 1),
                quarter_date_end=date(2024, 11, 30),
            ),
            Quarters(
                quarter_name="Вторая четверть",
                quarter_date_start=date(2024, 12, 1),
                quarter_date_end=date(2025, 2, 28),
            ),
            Quarters(
                quarter_name="Третья четверть",
                quarter_date_start=date(2025, 3, 1),
                quarter_date_end=date(2025, 5, 31),
            ),
            Quarters(
                quarter_name="Четвертая четверть",
                quarter_date_start=date(2025, 6, 1),
                quarter_date_end=date(2025, 8, 31),
            ),
        ]

        for quarter in quarters:
            session.add(quarter)

        await session.commit()

        for quarter in quarters:
            await session.refresh(quarter)

        # Insert the user and commit
        user = User(
            telegram_id=123123123,
            first_name="ASdd",
            last_name="dasd",
            username="asd",
            telegram_hash="asd",
            is_active=True,
        )
        session.add(user)

        # Commit the user before inserting grades
        await session.commit()
        await session.refresh(user)  # Refresh to ensure the user ID is available

        for _ in range(1, 10):
            grade = Grades(
                user_id=user.user_id,
                subject="Math",
                grade=randint(2, 5),  # Random grade between 1 and 5
                grade_weight=randint(1, 6),  # Random weight between 1 and 6
                grading_date=date(2024, 9, 1)
                + timedelta(days=randint(0, 120)),  # More variability in dates
            )
            session.add(grade)
            grade = NewGrades(
                grade_id=grade.grade_id,
                user_id=user.user_id,
                subject="Math",
                grade=randint(2, 5),  # Random grade between 1 and 5
                grade_weight=randint(1, 6),  # Random weight between 1 and 6
                grading_date=date(2024, 9, 1)
                + timedelta(days=randint(0, 120)),  # More variability in dates
            )
            session.add(grade)
        await session.commit()

    await db_manager.close()


asyncio.run(main())
