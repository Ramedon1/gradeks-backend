from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)

import settings


def get_play_now_keyboard():
    url = settings.WEB_UI_URL

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎇 Поехали", web_app=WebAppInfo(url=url)),
            ],
            [
                InlineKeyboardButton(
                    text="Сообщество Gradeks", url="https://t.me/gradeks"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎓 Как привязать дневник",
                    url="https://telegra.ph/Instrukciya-po-privyazke-ehlektronnogo-dnevnika-deeduorbru-k-Gradeks-12-15",
                )
            ],
        ]
    )
    return keyboard
