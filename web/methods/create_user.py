from db.manager import db_manager
from db.models.users import User
from tg.bot import bot
from web.models.users.telegram import WebAppInitData


async def create_users(telegram_data: WebAppInitData) -> User:
    user = await db_manager.users.create_user(
        telegram_id=telegram_data.user.id,
        first_name=telegram_data.user.first_name,
        last_name=telegram_data.user.last_name,
        username=telegram_data.user.username,
        telegram_hash=telegram_data.hash,
    )

    await db_manager.distribution.create_distributions_user(user_id=user.user_id)

    if telegram_data.start_param:
        print(telegram_data.start_param)
        print(telegram_data.start_param.split("_")[1])
        await db_manager.referral.set_referral(
            user_id=user.user_id,
            invited_by=int(telegram_data.start_param.split("_")[1]),
        )
        await bot.send_message(
            int(telegram_data.start_param.split("_")[1]),
            f"🎉 Вы пригласили друга, осталось совсем немного до получения бонусов!",
        )
    else:
        await db_manager.referral.set_referral(user_id=user.user_id, invited_by=None)

    return user
