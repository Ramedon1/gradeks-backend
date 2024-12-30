from aiogram.filters.callback_data import CallbackData
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)


class TaskCallbackData(CallbackData, prefix="task"):
    action: str
    task: str


def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌟 Активировать таску", callback_data="activate_task"
                ),
                InlineKeyboardButton(
                    text="🗑 Деактивировать таску", callback_data="deactivate_task"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔗 Привязать дневник пользователю",
                    callback_data="connect_diary_to_user",
                )
            ],
        ]
    )
    return keyboard


def get_tasks_keyboard(action: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Проверка оценок",
                    callback_data=TaskCallbackData(
                        action=action, task="scheduler"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="📝 Проверка финальных оценок",
                    callback_data=TaskCallbackData(
                        action=action, task="scheduler_finally"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Назад", callback_data="back_to_admin_menu"
                ),
            ],
        ]
    )
    return keyboard
