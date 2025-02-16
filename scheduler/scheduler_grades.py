import asyncio
import logging
from datetime import timedelta, datetime

from db.manager import db_manager
from scheduler.methods.common import get_full_year
from scheduler.methods.grade_control import GRADE_CHECKING_ENABLED
from scheduler.methods.grades import update_grades
from scheduler.methods.web import get_grades_by_period

logger = logging.getLogger(__name__)


async def process_user_grades(user):
    if not GRADE_CHECKING_ENABLED:
        logger.info(f"Проверка оценок отключена – пропускаем пользователя {user.user_id}")
        return

    quarters = await db_manager.periods.get_periods_by_period_name("quarter")
    start_date, end_date = await get_full_year(quarters)
    if not start_date or not end_date:
        return

    new_grades = await get_grades_by_period(user.diary_id, start_date, end_date)
    if new_grades:
        try:
            await update_grades(user.user_id, new_grades)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(f"Ошибка при обновлении оценок для пользователя {user.user_id}: {e}")


async def update_grades_task():
    users_diary_connected = await db_manager.users.user_scheduler_grades()
    if not users_diary_connected:
        logger.info("Нет пользователей для обновления оценок.")
        return

    tasks = [process_user_grades(user) for user in users_diary_connected]
    await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    while True:
        await update_grades_task()
        await asyncio.sleep(15)
