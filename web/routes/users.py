import re
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import FileResponse
from scheduler.methods.grades import add_grades

from db.manager import db_manager
from rediska import redis_manager
from tg.bot import bot
from web.depends.access_token import current_user_id
from web.exceptions.users import DiaryIdDException
from web.methods.create_user import create_users
from web.methods.fetch_user_data import fetch_user_data
from web.models.users.login import LoginRequest, LoginResponse
from web.models.users.user import DiaryConnect, SpecDiaryInfo, UserInfo

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/login")
async def login(login_data: LoginRequest) -> LoginResponse:
    """
    Если данные пришли, значит они успешно прошли проверку хеша и валидны
    Args:
        login_data: данные для входа, содержат сведения о пользователе

    Returns:
        (LoginResponse) Содержит токен и время сервера для монотонных часов
    """
    user = await db_manager.users.get_user_by_telegram_id(
        login_data.telegram_data.user.id
    )

    if user is None:
        user = await create_users(login_data.telegram_data)

    access_token = await redis_manager.access_tokens.create_access_token(user.user_id)
    return LoginResponse(access_token=access_token)


@user_router.get("/me")
async def get_me(user_id: Annotated[str, Depends(current_user_id)]) -> UserInfo:
    user = await db_manager.users.get_user(user_id)

    if user.is_active is False:
        return UserInfo(is_active=user.is_active)

    return await fetch_user_data(user_id)


@user_router.post("/link")
async def link_diary(
    user_id: Annotated[str, Depends(current_user_id)], request: DiaryConnect
) -> SpecDiaryInfo:
    match = re.search(r"participant=([\w\d]+)", request.diary_id)
    if not match:
        raise DiaryIdDException

    diary_id = match.group(1)

    await add_grades(user_id)

    telegram_id = await db_manager.users.get_telegram_id_by_user_id(user_id)
    await bot.send_message(
        telegram_id,
        f"🎉 Дневник успешно привязан, оценки доступны в приложении!",
    )
    await db_manager.users.connect_diary(user_id, diary_id)

    return SpecDiaryInfo(diary_id=diary_id, diary_link=True)


@user_router.get("/avatar/{tg_id}")
async def get_avatar(tg_id: str) -> FileResponse:
    image_path = Path(f"avatars/{tg_id}_avatar.jpg")
    if not image_path.is_file():
        return FileResponse(f"avatars/default_avatar.png")
    return FileResponse(image_path)
