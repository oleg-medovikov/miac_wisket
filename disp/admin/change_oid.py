from disp.admin import router
from aiogram import F, Bot
from aiogram.types import Message

from func import delete_message, update_message, add_keyboard
from mdls import Struct, User
from conf import CallAny


@router.message(F.text.startswith("oid"))
async def change_oid(message: Message, bot: Bot):
    """когда админ хочет заменить свой oid для отладки"""
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    dict_ = {"назад": CallAny(action="start").pack()}

    try:
        number = str(message.text).split(" ")[-1]
    except Exception:
        mess = "не нашел номера в сообщении"
        return await update_message(
            bot, message, mess, add_keyboard(dict_), image_name="admin"
        )

    struct = await Struct.get(number)
    if not struct:
        mess = f"неправильный oid {number}"
        return await update_message(
            bot, message, mess, add_keyboard(dict_), image_name="admin"
        )

    await user.update(oid=number).apply()
    mess = f"поменял ваш oid на {number}"
    return await update_message(
        bot, message, mess, add_keyboard(dict_), image_name="admin"
    )
