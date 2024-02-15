from disp.admin import router
from aiogram import F, Bot
from aiogram.types import Message
import logging

from func import delete_message, update_message, add_keyboard, get_time_lose
from mdls import User
from conf import CallAny


@router.message(F.text.startswith("time_lose"))
async def time_lose(message: Message, bot: Bot):
    """когда админ хочет заполнить в журнале time_lose вручную"""
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    dict_ = {"назад": CallAny(action="start").pack()}

    mess = ""

    try:
        await get_time_lose()
    except Exception as e:
        logging.error(str(e))
        mess = "не получилось сделать"
    else:
        mess = "Я закончил проставлять time\_lose без проблем"

    logging.info(mess)

    return await update_message(
        bot, message, mess, add_keyboard(dict_), image_name="admin"
    )
