import logging
from collections import defaultdict
from datetime import datetime

from db.manager import db_manager
from db.models.grades import Grades
from rediska import redis_manager
from scheduler.methods.common import get_full_year
from scheduler.methods.web import get_grades_by_period
from tg.bot import bot
from tg.common.web_app_keyboard import go_web_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def update_grades(user_id, new_grades):
    logger.info(f"Updating grades for user_id: {user_id}")
    telegram_id = await db_manager.users.get_telegram_id_by_user_id(user_id)
    existing_grades = await db_manager.grades.get_grades_by_user(user_id)
    existing_grades_map = {(g.subject, g.grading_date): g for g in existing_grades}

    processed_keys = set()
    new_grades_count = defaultdict(int)

    for new_grade in new_grades:
        for grade_entry in new_grade.grades:
            grading_date = datetime.strptime(grade_entry.date, "%Y-%m-%d").date()

            grade_key = (new_grade.subject, grading_date)
            processed_keys.add(grade_key)
            new_grades_count[new_grade.subject] += 1

            if grade_key in existing_grades_map:
                existing_grade = existing_grades_map[grade_key]

                if (
                    existing_grade.grade != grade_entry.grade
                    and existing_grade.grade_weight != grade_entry.weight
                ):
                    logger.info(f"Updating grade for {grade_key}")
                    await db_manager.grades.change_grade(
                        grade_id=existing_grade.grade_id,
                        new_grade=grade_entry.grade,
                        grade_weight=grade_entry.weight,
                    )
                    await redis_manager.new_grades.update_grade_in_redis(
                        user_id=user_id,
                        subject=new_grade.subject,
                        grading_date=grading_date.strftime("%d-%m"),
                        new_grade=grade_entry.grade,
                        old_grade=existing_grade.grade,
                        grade_weight=grade_entry.weight,
                    )

                    await bot.send_message(
                        chat_id=telegram_id,
                        text=f'🔃 Обновили оценку на {existing_grade.grading_date.strftime("%d.%m.%Y")}. \n'
                        f"📚 Предмет: {existing_grade.subject} \n"
                        f"Была оценка: {existing_grade.grade} | Стала оценка: {grade_entry.grade}",
                        reply_markup=go_web_app(),
                    )
            else:
                logger.info(f"Adding new grade for {grade_key}")
                new_db_grade = Grades(
                    user_id=user_id,
                    subject=new_grade.subject,
                    grading_date=grading_date,
                    grade=grade_entry.grade,
                    grade_weight=grade_entry.weight,
                )
                await db_manager.grades.add_grade(new_db_grade)

                await redis_manager.new_grades.add_new_grade_to_redis(
                    user_id=user_id,
                    subject=new_grade.subject,
                    grading_date=grading_date.strftime("%d-%m"),
                    grade=grade_entry.grade,
                    grade_weight=grade_entry.weight,
                )

                await bot.send_message(
                    chat_id=telegram_id,
                    text=f"🗓 Новая оценка. \n"
                    f"📚 Предмет: {new_db_grade.subject} \n"
                    f'Оценка: {new_db_grade.grade} | {new_db_grade.grading_date.strftime("%d.%m.%Y")}',
                    reply_markup=go_web_app(),
                )

    for existing_grade in existing_grades:
        grade_key = (existing_grade.subject, existing_grade.grading_date)

        if grade_key not in processed_keys:
            if new_grades_count[existing_grade.subject] > 0:
                new_grades_count[existing_grade.subject] -= 1
                logger.info(f"Removing outdated grade for {grade_key}")
                await db_manager.grades.delete_grade(existing_grade.grade_id)

    logger.info(f"Grades updated successfully for user_id: {user_id}")


async def add_grades(user_id, diary_id):
    quarters = await db_manager.periods.get_periods_by_name("quarter")
    start_date, end_date = await get_full_year(quarters)

    if (start_date, end_date) is None:
        logger.error("Failed to get current period")
        raise "Failed to get current period"

    new_grades = await get_grades_by_period(diary_id, start_date, end_date)
    logger.info(f"First adding grades for user_id: {user_id}")

    if len(new_grades) > 0:
        existing_grades = await db_manager.grades.get_grades_by_user(user_id)
        existing_grades_map = {(g.subject, g.grading_date): g for g in existing_grades}

        for new_grade in new_grades:
            for grade_entry in new_grade.grades:
                grading_date = datetime.strptime(grade_entry.date, "%Y-%m-%d").date()
                grade_key = (new_grade.subject, grading_date)

                if grade_key in existing_grades_map:
                    logger.info(f"Grade for {grade_key} already exists. Skipping.")
                    continue

                new_db_grade = Grades(
                    user_id=user_id,
                    subject=new_grade.subject,
                    grading_date=grading_date,
                    grade=grade_entry.grade,
                    grade_weight=grade_entry.weight,
                )

                await db_manager.grades.add_grade(new_db_grade)

        logger.info(f"Grades added successfully for user_id: {user_id}")
    else:
        logger.error("Failed to get grades from web")
        raise "Failed to get grades from web"
