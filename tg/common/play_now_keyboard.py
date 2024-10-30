from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)

import settings


def get_play_now_keyboard(ref: int | str | None = None):
    url = settings.WEB_UI_URL
    if ref:
        url += f"?tgWebAppStartParam=r_{ref}"

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
                    text="🎓 Как привязать", url="https://t.me/gradeks/3"
                )
            ],
            # TODO Сделать туториал по привязке дневника
        ]
    )
    return keyboard
