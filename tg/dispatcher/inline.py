import os
import shutil
from io import BytesIO
from aiogram.types import BufferedInputFile

from aiogram import Router
from aiogram.enums import InputMediaType, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (ChosenInlineResult, FSInputFile, InlineQuery,
                           InlineQueryResultAudio, InputMediaAudio, Message, InlineQueryResultCachedAudio,
                           InputMediaPhoto)
from sqlalchemy.testing.suite.test_reflection import users

import settings
from db.manager import db_manager
from imagination.day_grade import day_grade_img
from imagination.quarter_grade import img_quarter_grade
from imagination.subject_grade import subject_grade_img
from rediska import redis_manager
from tg.bot import bot
from tg.common.keyboards.inline_keyboard import inline_send
from web.methods.get_diary_info import get_old_grade, get_new_grade, get_diary_info, get_diary_info_by_period
from web.methods.get_user_info import get_new_grades


inline_router = Router()

periods_data = {
    'Первое полугодие': {
        'title': 'Первое полугодие',
        'id': 'semester_one',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMpZ1n7zeAJGH9toBeCw1IAAW-Dns-pAAJIWQACjZHQSu1wVjNIJpEuNgQ',
    },
    'Второе полугодие': {
        'title': 'Второе полугодие',
        'id': 'semester_two',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMqZ1n7zQsThs5GFPg4UTjY6cOzWXQAAklZAAKNkdBKfpouJxp403U2BA',
    },
    'Первая четверть': {
        'title': 'Первая четверть',
        'id': 'quarter_first',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMlZ1n7xiKLseYBYNuCwEWCXbg08NcAAkRZAAKNkdBK2ni6e0hjwoA2BA',
    },
    'Вторая четверть': {
        'title': 'Вторая четверть',
        'id': 'quarter_second',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMmZ1n7zBWF7bumSLKLdd6u_DIneVgAAkVZAAKNkdBK06A9ZPDe1Hs2BA',
    },
    'Третья четверть': {
        'title': 'Третья четверть',
        'id': 'quarter_third',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMnZ1n7zGjKQjhSoVb_3uL3rO0wQRMAAkZZAAKNkdBKVo0HwjCyoAg2BA',
    },
    'Четвертая четверть': {
        'title': 'Четвертая четверть',
        'id': 'quarter_fourth',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMoZ1n7zKC8tJtF7uskvFnvnNhXSfoAAkdZAAKNkdBKwgQa2kJf7uM2BA',
    },
    'Все оценки': {
        'title': 'Все оценки',
        'id': 'year',
        'audio_file_id': 'CQACAgIAAyEGAASPGL1TAAMrZ1n70danILltuO8KglyI0VbGUdUAAkpZAAKNkdBKBg3fjK1vhMc2BA',
    },
}


@inline_router.inline_query()
async def inline_query(inline_query: InlineQuery):
    user = await db_manager.users.get_user_by_telegram_id(inline_query.from_user.id)

    if user is None:
        return await bot.answer_inline_query(
            inline_query.id,
            is_personal=True,
            results=[],
            switch_pm_text="Привязать дневник",
            switch_pm_parameter="connect",
            cache_time=0,
        )

    user_new_grades = await get_new_grades(user.user_id)
    user_grades = await db_manager.grades.get_grades_by_user(user.user_id)

    results = []

    if inline_query.query != '':
        subject = await db_manager.grades.get_subject_name_by_ilike_subject(user.user_id, inline_query.query)
        if subject is not None:
            audio = await bot.send_audio(
                chat_id='-1002400763219',
                audio=FSInputFile(path='static/basic.mp3', filename='../../static/basic.mp3'),
                title=f"{subject[:17]} - все оценки",
                caption=f"🔁 Загрузка ...",
            )

            results.append(
                InlineQueryResultCachedAudio(
                    id=f'all_{subject[:15]}',
                    audio_file_id=audio.audio.file_id,
                    title=f"{subject[:17]} - все оценки",
                    caption=f"🔁 Загрузка ...",
                    reply_markup=inline_send()
                )
            )

    if len(user_grades) == 0 and user_new_grades == []:
        return await bot.answer_inline_query(
            inline_query.id,
            is_personal=True,
            results=[],
            switch_pm_text="Похоже, у вас нет оценок 😕",
            switch_pm_parameter="no_grades",
            cache_time=0,
        )

    if user_new_grades is not []:
        for grade in user_new_grades:
            audio = await bot.send_audio(
                chat_id='-1002400763219',
                audio=FSInputFile(path='static/basic.mp3', filename='../../static/basic.mp3'),
                title=f"{str(grade.subject[:17] + '...') if len(grade.subject) >= 17 else grade.subject} - {grade.grade}",
                caption=f"🔁 Загрузка ...",
            )

            results.append(
                InlineQueryResultCachedAudio(
                    id=f'last_{grade.grade}_{grade.subject[:10]}_{grade.date}_{grade.coff}',
                    audio_file_id=audio.audio.file_id,
                    title=f"{str(grade.subject[:17] + '...') if len(grade.subject) >= 17 else grade.subject} - {grade.grade}",
                    caption=f"🔁 Загрузка ...",
                    reply_markup=inline_send()
                )
            )
    if len(user_grades) > 0:
        for period_name, period_data in periods_data.items():
            results.append(
                InlineQueryResultCachedAudio(
                    id=period_data['id'],
                    audio_file_id=period_data['audio_file_id'],
                    title=f"{period_data['title']}",
                    caption=f"🔁 Загрузка ...",
                    reply_markup=inline_send(),
                    parse_mode=ParseMode.MARKDOWN,
                )
            )

    await bot.answer_inline_query(
        inline_query.id,
        results=results,
        is_personal=True,
        cache_time=0,
    )




@inline_router.chosen_inline_result()
async def handle_chosen_result(chosen_result: ChosenInlineResult):
    if chosen_result.result_id.split('_')[0] == 'all':
        user = await db_manager.users.get_user_by_telegram_id(chosen_result.from_user.id)
        subject = await db_manager.grades.get_subject_name_by_ilike_subject(user.user_id,
                                                                            chosen_result.result_id.split('_')[1])
        grades = await db_manager.grades.get_grades_by_subject(user.user_id, subject)

        img = await subject_grade_img(subject, get_new_grade(grades), get_old_grade(grades), grades)

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        input_file = BufferedInputFile(
            file=img_byte_arr.getvalue(),
            filename="grades_image.png"
        )

        photo = await bot.send_photo(
            chat_id='-1002400763219',
            photo=input_file,
        )

        await chosen_result.bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo.photo[-1].file_id,
                caption=f"📊 Оценки по {subject}",
            ),
            inline_message_id=chosen_result.inline_message_id,
            reply_markup=inline_send(),
        )
    if chosen_result.result_id.split('_')[0] == 'last':
        grade = chosen_result.result_id.split('_')[1]
        date = chosen_result.result_id.split('_')[3]
        coff = chosen_result.result_id.split('_')[4]
        user = await db_manager.users.get_user_by_telegram_id(chosen_result.from_user.id)

        subject = await db_manager.grades.get_subject_name_by_ilike_subject(user.user_id,
                                                                            chosen_result.result_id.split('_')[2])
        img = await day_grade_img(date=date, subject=subject, grade=grade, coff=coff)

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        input_file = BufferedInputFile(
            file=img_byte_arr.getvalue(),
            filename="grades_image.png"
        )

        photo = await bot.send_photo(
            chat_id='-1002400763219',
            photo=input_file,
        )
        await chosen_result.bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo.photo[-1].file_id,
                caption=f"🗓 Последняя оценка по {subject} за {date}",
            ),
            inline_message_id=chosen_result.inline_message_id,
            reply_markup=inline_send(),
        )
    if chosen_result.result_id in [data['id'] for data in periods_data.values()]:
        # Find the corresponding period name
        period_name = next(
            (data['title'] for data in periods_data.values() if data['id'] == chosen_result.result_id),
            None
        )
        if period_name:
            user = await db_manager.users.get_user_by_telegram_id(chosen_result.from_user.id)
            data_quarter = await get_diary_info_by_period(user.user_id, period_name)

            img = await img_quarter_grade(data_quarter, period_name)

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

            input_file = BufferedInputFile(
                file=img_byte_arr.getvalue(),
                filename="grades_image.png"
            )

            photo = await bot.send_photo(
                chat_id='-1002400763219',
                photo=input_file,
            )

            await chosen_result.bot.edit_message_media(
                media=InputMediaPhoto(
                    media=photo.photo[-1].file_id,
                    caption=f"☕️ Все оценки за {period_name}",
                ),
                inline_message_id=chosen_result.inline_message_id,
                reply_markup=inline_send(),
            )
