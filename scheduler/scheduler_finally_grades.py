import asyncio

from db.manager import db_manager
from scheduler.methods.grades import add_new_finally_grades
from scheduler.methods.web import get_final_grades


async def process_user_grades(user):
    new_grades = await get_final_grades(user.diary_id)
    if new_grades:
        try:
            await add_new_finally_grades(user.user_id, new_grades)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            pass


async def update_finally_grades_task():
    users_diary_connected = await db_manager.users.user_scheduler_grades()
    if not users_diary_connected:
        return

    tasks = [process_user_grades(user) for user in users_diary_connected]
    await asyncio.gather(*tasks)


async def main():
    while True:
        await update_finally_grades_task()
        await asyncio.sleep(600)
