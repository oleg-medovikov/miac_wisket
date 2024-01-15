from disp.start import router
from typing import Optional
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F, Bot
from datetime import datetime

from mdls import User, UserLog
from conf import CallAny
from func import (
    delete_message,
    update_message,
    add_keyboard,
    get_chat_fio,
    hello_message,
)


@router.message(CommandStart())
@router.callback_query(CallAny.filter(F.action == "start"))
async def command_start_handler(
    mess: Message | CallbackQuery, bot: Bot, callback_data: Optional[CallAny] = None
):
    """
    начальная команда бота,одновременно отрабатывает команду start и салбек с экшеном start
    """
    if isinstance(mess, CallbackQuery) and isinstance(mess.message, Message):
        chat_id = mess.message.chat.id
        message = mess.message
    elif isinstance(mess, Message):
        await delete_message(mess)
        chat_id = mess.chat.id
        message = mess
    else:
        return

    user = await User.query.where(User.tg_id == chat_id).gino.first()
    if user is None:
        if isinstance(mess, Message):
            await UserLog.create(
                time=datetime.now(),
                event=f"Неизвестный пользователь {chat_id} {get_chat_fio(mess)}",
            )
        return None

    DICT = {}

    if not callback_data:
        callback_data = CallAny(action="watch_workers", user_id=user.id)

    # DICT["Ваши работники"] = callback_data.pack()

    if user.admin:
        callback_data.action = "settings"
        DICT["настройки"] = callback_data.pack()

    print(DICT)
    await update_message(
        bot, message, hello_message(user), add_keyboard(DICT), image_name="main"
    )
