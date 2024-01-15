from typing import Optional
from aiogram.types import InputMediaPhoto, Message, InlineKeyboardMarkup
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods.edit_message_media import EditMessageMedia
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from aiogram import Bot
import logging

from mdls import Image, MessLog


async def update_message(
    bot: Bot,
    message: Optional[Message],
    MESS: str,
    keyboard: Optional[InlineKeyboardMarkup],
    html: bool = False,
    image_id: Optional[int] = None,
    image_name: Optional[str] = None,
):
    """
    изменение сообщения с обработкой исключений
    запара с наличием пользовательских картинок, которые необходимо не перепутать с
    """
    if message is None:
        return

    mode = "html" if html else "Markdown"

    # ищем логи сообщений
    log = await MessLog.query.where(MessLog.tg_id == message.chat.id).gino.first()
    # ищем картинку в базе
    if image_id:
        image = await Image.get(image_id)
    elif image_name:
        image = await Image.query.where(Image.name == image_name).gino.first()
    else:
        image = None
        # если не указана картинка смотрим, что там в логе
        if log and log.image_id:
            if "user" in log.name:
                image = await Image.get(log.image_id)

    # в любом случае удаляем комманду пользователя, так как  она не нужна
    if log and log.mess_id != message.message_id:
        await _delete_mess(bot, message.chat.id, message.message_id)

    if log and image:
        # если сообщение есть, то нужно его апдейтить
        try:
            await bot(
                EditMessageMedia(
                    chat_id=log.tg_id,
                    message_id=log.mess_id,
                    # надо достать айдишник картинки с серверов телеги
                    media=InputMediaPhoto(
                        media=image.file_id, caption=MESS, parse_mode=mode
                    ),
                    reply_markup=keyboard,
                )
            )
            await log.update(image_id=image.id).apply()
        except TelegramBadRequest as e:
            logging.error(f"!!!! не удалось изменить картинку \n{str(e)}")
            # если не удалось апдейтить, то удалем и шлём новое
            await _delete_mess(bot, log.tg_id, log.mess_id)
            await _send_new_mess(message, MESS, keyboard, mode, image)
    else:
        await _send_new_mess(message, MESS, keyboard, mode, None)


async def _delete_mess(bot, chat_id: int, mess_id: int):
    """обрабатываю исключения"""
    try:
        await bot(DeleteMessage(chat_id=chat_id, message_id=mess_id))
    except TelegramBadRequest as e:
        logging.error(
            "!!!! не удалось удалить сообщение, неправильный реквест\n" + str(e)
        )
    except TelegramNotFound:
        logging.error("!!!! не удалось удалить сообщение, не найдено")


async def _send_new_mess(message, MESS, keyboard, mode, image):
    # если нет логов, то нужно отправить новое сообщение и записать его в логи
    if image:
        message = await message.answer_photo(
            # BufferedInputFile(image.file, filename=image.name + ".png"),
            photo=image.file_id,
            caption=MESS,
            parse_mode=mode,
            reply_markup=keyboard,
        )
        await MessLog.delete.where(MessLog.tg_id == message.chat.id).gino.status()
        await MessLog.create(
            tg_id=message.chat.id, mess_id=message.message_id, image_id=image.id
        )
        return message
    else:
        # вариант без картинки
        message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)
        await MessLog.delete.where(MessLog.tg_id == message.chat.id).gino.status()
        await MessLog.create(tg_id=message.chat.id, mess_id=message.message_id)
