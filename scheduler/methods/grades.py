import logging
from datetime import datetime
from uuid import UUID

from db.manager import db_manager
from db.models.grades import Grades
from rediska import redis_manager
from scheduler.methods.common import get_full_year
from scheduler.methods.web import get_grades_by_period, get_final_grades
from scheduler.models import GradeFinal
from tg.bot import bot
from tg.common.keyboards.web_app_keyboard import go_web_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def update_grades(user_id, new_grades):
    logger.info(f"Updating grades for user_id: {user_id}")
    telegram_id = await db_manager.users.get_telegram_id_by_user_id(user_id)

    # Retrieve existing grades from the database
    existing_grades = await db_manager.grades.get_grades_by_user(user_id)
    existing_grades_map = {(g.subject, g.grading_date): g for g in existing_grades}

    # Map new grades by (subject, grading_date)
    new_grades_map = {
        (
            new_grade.subject,
            datetime.strptime(grade_entry.date, "%Y-%m-%d").date(),
        ): grade_entry
        for new_grade in new_grades
        for grade_entry in new_grade.grades
    }

    # Sets of grade keys for efficient comparison
    existing_keys = set(existing_grades_map.keys())
    new_keys = set(new_grades_map.keys())

    # Grades to add, update, and delete
    keys_to_add = new_keys - existing_keys
    keys_to_update = existing_keys & new_keys
    keys_to_delete = existing_keys - new_keys

    # Process updates
    for key in keys_to_update:
        existing_grade = existing_grades_map[key]
        new_grade_entry = new_grades_map[key]

        if (
            existing_grade.grade != new_grade_entry.grade
            or existing_grade.grade_weight != new_grade_entry.weight
        ):
            logger.info(f"Updating grade for {key}")
            await db_manager.grades.change_grade(
                grade_id=existing_grade.grade_id,
                new_grade=new_grade_entry.grade,
                grade_weight=new_grade_entry.weight,
            )
            await redis_manager.new_grades.update_grade_in_redis(
                user_id=user_id,
                subject=key[0],
                grading_date=key[1].strftime("%d-%m"),
                new_grade=new_grade_entry.grade,
                old_grade=existing_grade.grade,
                grade_weight=new_grade_entry.weight,
            )
            try:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=f"🔃 Обновили оценку на {key[1].strftime('%d.%m.%Y')}. \n"
                    f"📚 Предмет: {existing_grade.subject} \n"
                    f"Была оценка: {existing_grade.grade} | Стала оценка: {new_grade_entry.grade} | Вес оценки: {new_grade_entry.weight}",
                    reply_markup=go_web_app(),
                )
            except:
                pass

    # Process additions
    for key in keys_to_add:
        subject, grading_date = key
        grade_entry = new_grades_map[key]
        logger.info(f"Adding new grade for {key}")

        new_db_grade = Grades(
            user_id=user_id,
            subject=subject,
            grading_date=grading_date,
            grade=grade_entry.grade,
            grade_weight=grade_entry.weight,
        )
        await db_manager.grades.add_grade(new_db_grade)
        await redis_manager.new_grades.add_new_grade_to_redis(
            user_id=user_id,
            subject=subject,
            grading_date=grading_date.strftime("%d-%m"),
            grade=grade_entry.grade,
            grade_weight=grade_entry.weight,
        )
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=f"🗓 Новая оценка. \n"
                f"📚 Предмет: {new_db_grade.subject} \n"
                f"Оценка: {new_db_grade.grade} | {new_db_grade.grading_date.strftime('%d.%m.%Y')} | Вес оценки: {new_db_grade.grade_weight}",
                reply_markup=go_web_app(),
            )
        except:
            pass

    for key in keys_to_delete:
        existing_grade = existing_grades_map[key]
        logger.info(f"Removing outdated grade for {key}")
        await db_manager.grades.delete_grade(existing_grade.grade_id)
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=f"🗑 Удалена оценка \n"
                f"📚 Предмет: {existing_grade.subject} \n"
                f"Оценка: {existing_grade.grade} | {existing_grade.grading_date.strftime('%d.%m.%Y')}",
                reply_markup=go_web_app(),
            )
        except:
            pass
    logger.info(f"Grades updated successfully for user_id: {user_id}")


async def add_grades(user_id, diary_id):
    quarters = await db_manager.periods.get_periods_by_period_name("quarter")
    start_date, end_date = await get_full_year(quarters)

    if (start_date, end_date) is None:
        logger.error("Failed to get current period")
        raise "Failed to get current period"

    new_grades = await get_grades_by_period(diary_id, start_date, end_date)
    logger.info(f"First adding grades for user_id: {user_id}")

    if len(new_grades) > 0:
        existing_diary = await db_manager.grades.get_grades_by_user(user_id)
        if len(existing_diary) > 0:
            await db_manager.users.disconnect_diary(user_id)
            await db_manager.grades.delete_grades_by_user(user_id)

        for new_grade in new_grades:
            for grade_entry in new_grade.grades:
                grading_date = datetime.strptime(grade_entry.date, "%Y-%m-%d").date()

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


async def add_new_finally_grades(user_id: str | UUID, new_grades: list[GradeFinal]):
    """
    Add or update final grades for a user based on the GradeFinal model.

    Args:
        user_id (str | UUID): Unique identifier for the user.
        new_grades (list[GradeFinal]): List of GradeFinal objects containing periods and grades.

    Raises:
        Exception: If there's an issue with adding or updating grades.
    """

    logger.info(f"Adding or updating final grades for user_id: {user_id}")

    telegram_id = await db_manager.users.get_telegram_id_by_user_id(user_id)

    existing_finally_grades = (
        await db_manager.grades_finally.get_finally_grades_by_user_id(user_id)
    )
    existing_finally_grades_map = {
        (g.subject, g.quarter): g for g in existing_finally_grades
    }

    for grade_final in new_grades:
        subject = grade_final.subject

        for period in grade_final.periods:
            quarter = period.name

            if not period.grades or isinstance(period.grades, str):
                logger.info(f"No grades provided for {subject} in {quarter}. Skipping.")
                continue

            final_grade = max((grade.grade for grade in period.grades), default=None)

            if final_grade is None:
                logger.info(f"No valid grades for {subject} in {quarter}. Skipping.")
                continue

            grade_key = (subject, quarter)

            if grade_key in existing_finally_grades_map:
                existing_grade = existing_finally_grades_map[grade_key]

                if existing_grade.grade != final_grade:
                    logger.info(f"Updating final grade for {grade_key}")

                    await redis_manager.new_grades.update_grade_in_redis(
                        user_id=user_id,
                        subject=subject,
                        grading_date=quarter,
                        new_grade=final_grade,
                        old_grade=existing_grade.grade,
                        grade_weight=1,
                    )

                    await bot.send_message(
                        chat_id=telegram_id,
                        text=f"🔃 Обновлена итоговая оценка по {subject} \n"
                        f"📅 {quarter} \n"
                        f"📊 Была оценка: {'Зачёт' if existing_grade.grade == 0 else existing_grade.grade} | Стала оценка: {'Зачёт' if final_grade == 0 else final_grade}",
                        reply_markup=go_web_app(),
                    )

                    await db_manager.grades_finally.change_finally_grade(
                        user_id=user_id,
                        new_grade=int(final_grade),
                        subject=subject,
                        quarter=quarter,
                    )
                else:
                    logger.info(f"Final grade for {grade_key} is unchanged. Skipping.")
            else:
                logger.info(f"Adding new final grade for {grade_key}")
                await redis_manager.new_grades.add_new_grade_to_redis(
                    user_id=user_id,
                    subject=subject,
                    grading_date=quarter,
                    grade=final_grade,
                    grade_weight=1,
                    is_final=True,
                )
                await bot.send_message(
                    chat_id=telegram_id,
                    text=f"👏 Выставлена итоговая оценка по {subject} \n"
                    f"📅 {quarter} \n"
                    f"📊 Оценка: {'Зачёт' if final_grade == 0 else final_grade}",
                    reply_markup=go_web_app(),
                )
                await db_manager.grades_finally.add_finally_grade(
                    user_id=user_id,
                    grade=int(final_grade),
                    subject=subject,
                    quarter=quarter,
                )

    logger.info(f"Final grades updated successfully for user_id: {user_id}")


async def add_finally_grades(user_id: str | UUID, diary_id: str):
    """
    Add final grades for a user based on the GradeFinal model.

    Args:
        user_id (str | UUID): Unique identifier for the user.

    Raises:
        Exception: If there's an issue with adding grades.
    """
    new_grades = await get_final_grades(diary_id)

    if not new_grades:
        logger.info(f"No final grades to add for user_id: {user_id}")
        raise "Failed to get grades from web"

    logger.info(f"Adding final grades for user_id: {user_id}")

    existing_diary = await db_manager.grades_finally.get_finally_grades_by_user_id(
        user_id
    )

    if len(existing_diary) > 0:
        await db_manager.users.disconnect_diary(user_id)
        await db_manager.grades_finally.delete_finally_grades_by_user_id(user_id)

    for grade_final in new_grades:
        subject = grade_final.subject

        for period in grade_final.periods:
            quarter = period.name

            if not period.grades or isinstance(period.grades, str):
                logger.info(f"No grades provided for {subject} in {quarter}. Skipping.")
                continue

            final_grade = max((grade.grade for grade in period.grades), default=None)

            if final_grade is None:
                logger.info(f"No valid grades for {subject} in {quarter}. Skipping.")
                continue

            logger.info(f"Adding final grade for {subject} in {quarter}: {final_grade}")

            await db_manager.grades_finally.add_finally_grade(
                user_id=user_id,
                grade=int(final_grade),
                subject=subject,
                quarter=quarter,
            )

    logger.info(f"Final grades added successfully for user_id: {user_id}")
