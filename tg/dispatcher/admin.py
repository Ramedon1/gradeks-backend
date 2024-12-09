import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import settings
from common.common import log_task_exception
from db.manager import db_manager
from tg.bot import bot
from tg.common.keyboards.admin_keyboards import (TaskCallbackData,
                                                 get_admin_keyboard,
                                                 get_tasks_keyboard)
from tg.dispatcher.states import AdminLinkDiaryStates
from web.models.users.user import DiaryConnect
from web.routes.users import link_diary

admin_router = Router()


@admin_router.message(Command("admin"))
async def admin_menu(message: Message | CallbackQuery):
    if message.from_user.id == int(settings.ADMIN_ID):
        keyboard = get_admin_keyboard()

        tasks = [
            task.get_name()
            for task in asyncio.all_tasks()
            if task.get_name()[:5] != "Task-"
        ]

        tasks_str = "\n".join(tasks)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"👤 Количество пользователей: {len(await db_manager.users.get_all_users())}\n"
            f"📖 Пользователи, которые подключили дневник: {len(await db_manager.users.get_users_diary_connected())}\n"
            f"📚 Активные таски: {tasks_str}\n",
            reply_markup=keyboard,
            parse_mode="MarkdownV2",
        )


@admin_router.callback_query(F.data.in_({"activate_task", "deactivate_task"}))
async def handle_task(callback: CallbackQuery):
    await callback.answer()
    await bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id
    )
    action = "запустить" if callback.data == "activate_task" else "остановить"
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выберете таску, которую хотите {action}",
        reply_markup=get_tasks_keyboard(callback.data.split("_")[0]),
    )


@admin_router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: CallbackQuery):
    await callback.answer()
    await bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id
    )
    await admin_menu(callback)



@admin_router.callback_query(TaskCallbackData.filter())
async def handle_task_action(callback: CallbackQuery, callback_data: TaskCallbackData):
    action = callback_data.action
    task_name = callback_data.task

    await callback.answer()

    if action == "activate":
        if task_name == "scheduler":
            existing_task = next(
                (task for task in asyncio.all_tasks() if task.get_name() == task_name),
                None
            )
            if existing_task and not existing_task.done():
                await callback.message.answer(f"Таска {task_name} уже запущена.")
                return

            from scheduler.scheduler_grades import main

            task = asyncio.create_task(main(), name=task_name)

            task.add_done_callback(lambda t: asyncio.create_task(log_task_exception(t)))

            await callback.message.answer(f"Таска {task_name} запущена.")
        else:
            await callback.message.answer("Неизвестная таска.")

    elif action == "deactivate":
        existing_task = next(
            (task for task in asyncio.all_tasks() if task.get_name() == task_name),
            None
        )
        if existing_task and not existing_task.done():
            existing_task.cancel()
            await callback.message.answer(f"Таска {task_name} остановлена.")
        else:
            await callback.message.answer(f"Таска {task_name} не найдена или уже остановлена.")
    else:
        await callback.message.answer("Неизвестное действие.")


@admin_router.callback_query(F.data == "connect_diary_to_user")
async def connect_diary_to_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminLinkDiaryStates.telegram_id)
    await bot.send_message(
        chat_id=callback.from_user.id, text="Введите ID пользователя "
    )


@admin_router.message(AdminLinkDiaryStates.telegram_id)
async def find_user(message: Message, state: FSMContext):
    db_user_id = await db_manager.users.get_user_by_telegram_id(int(message.text))
    if db_user_id:
        await state.update_data(telegram_id=message.text, user_id=db_user_id)
        await state.set_state(AdminLinkDiaryStates.diary_id)
        await bot.send_message(chat_id=message.from_user.id, text="Введите ID дневника")
    else:
        await bot.send_message(
            chat_id=message.from_user.id, text="Пользователь не найден"
        )
        await state.clear()


@admin_router.message(AdminLinkDiaryStates.diary_id)
async def link_diary_admin(message: Message, state: FSMContext):
    data = await state.get_data()
    await link_diary(
        user_id=data["user_id"], request=DiaryConnect(diary_id=message.text)
    )
    await bot.send_message(chat_id=message.from_user.id, text="Дневник привязан")
    await state.clear()
