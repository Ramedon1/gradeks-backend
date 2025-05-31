from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

import settings


def go_web_app():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Открыть оценки",
                    web_app=WebAppInfo(url=settings.WEB_UI_URL),
                ),
            ],
        ]
    )
    return keyboard
