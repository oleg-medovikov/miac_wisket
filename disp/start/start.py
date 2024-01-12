from disp.start import router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot

from mdls import User, UserLog
from func import delete_message, get_chat_fio


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    """
    начальная команда бота
    """
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None:
        await UserLog.create(
            event=f"Неизвестный пользователь {message.chat.id} {get_chat_fio(message)}"
        )
        return None

    mess = "Добрый день, доступные Вам команды"

    DICT = {}

    DICT["Ваши работники"] = ("watch_workers",)

    await message.answer("привет!")
