import asyncio

from db.manager import db_manager
from scheduler.methods.common import get_current_period
from scheduler.methods.grades import update_grades
from scheduler.methods.web import get_grades_by_period



async def process_user_grades(user):
    quarters = await db_manager.quarters.get_quarters()
    start_date, end_date = await get_current_period(quarters)

    if not start_date or not end_date:
        return

    new_grades = await get_grades_by_period(user.diary_id, start_date, end_date)
    if new_grades:
        try:
            await update_grades(user.user_id, new_grades)
        except asyncio.CancelledError:
            pass
        except Exception:
            pass


async def update_grades_task():
    users_diary_connected = await db_manager.users.user_scheduler_grades()
    if not users_diary_connected:
        return

    tasks = [process_user_grades(user) for user in users_diary_connected]
    await asyncio.gather(*tasks)


async def main():
    while True:
        await update_grades_task()
        await asyncio.sleep(30)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
