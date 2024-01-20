from disp.base import router
from aiogram.types import Message
from aiogram import F, Bot
import logging

from func import (
    delete_message,
    update_message,
    add_keyboard,
    read_Struct,
    read_Worker,
)
from mdls import User
from conf import CallAny


@router.message(F.content_type.in_(["document"]))
async def read_excel(message: Message, bot: Bot):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        logger = logging.getLogger(__name__)
        logger.error("Прилетел файл от юзера без админских прав")
        return

    if message.document is None:
        logger = logging.getLogger(__name__)
        logger.error("В сообщении с файлом нет файла")
        return

    if " " in str(message.document.file_name):
        file_name = str(message.document.file_name).split(" ")[0] + ".xlsx"
    else:
        file_name = str(message.document.file_name)

    FUNC = {
        "Struct.xlsx": read_Struct(user),
        "Worker.xlsx": read_Worker(user),
    }.get(file_name)

    if FUNC is None:
        logger = logging.getLogger(__name__)
        logger.error("Нет функции для обработки файла")
        return

    file = await bot.get_file(message.document.file_id)
    await bot.download_file(str(file.file_path), f"/tmp/_{file_name}")

    dict_ = {"назад": CallAny(action="start").pack()}
    try:
        mess = await FUNC
    except Exception as e:
        await update_message(
            bot, message, str(e), keyboard=add_keyboard(dict_), image_name="update_base"
        )
    else:
        await update_message(
            bot, message, mess, keyboard=add_keyboard(dict_), image_name="update_base"
        )
