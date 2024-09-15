from db.manager import db_manager
from db.models.users import User
from web.models.users.telegram import WebAppInitData


async def create_user(telegram_data: WebAppInitData) -> User:

    user = await db_manager.users.create_user(
        telegram_id=telegram_data.user.id,
        first_name=telegram_data.user.first_name,
        last_name=telegram_data.user.last_name,
        username=telegram_data.user.username,
        telegram_hash=telegram_data.hash,
    )

    invited_by_id = None

    if telegram_data.start_param is not None and telegram_data.start_param.startswith(
        "r_"
    ):
        invited_by_tg_id = telegram_data.start_param.replace("r_", "")
        user = await db_manager.users.get_user_by_telegram_id(
            telegram_id=int(invited_by_tg_id)
        )
        if user is not None:
            invited_by_id = user.user_id

    await db_manager.referral.set_referral(user_id=telegram_data.user.id, invited_by=invited_by_id)


    return user
