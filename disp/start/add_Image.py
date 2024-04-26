from disp.start import router
from aiogram import F, Bot
from aiogram.types import Message, File
import logging

from func import delete_message, add_keyboard, update_message, get_chat_ids
from mdls import User, Image
from conf import CallAny


@router.message(F.content_type.in_(["photo"]))
async def add_Image(message: Message, bot: Bot):
    """
    проверить, есть ли такое изображение в базе и добавить его
    """
    await delete_message(message)
    await get_chat_ids(message, bot)

    if not message.photo:
        logger = logging.getLogger(__name__)
        logger.error("Произошла ошибка Нет картинки в сообщении")
        return

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or user.admin is False:
        logger = logging.getLogger(__name__)
        logger.error(
            "Произошла ошибка при отправке картинки на сработали админские права"
            + f"\nuser: {user} chat_id: {message.chat.id}"
        )
        return

    # Получаем объект photo
    photo = message.photo[-1]
    # Получаем файл объекта photo
    file = await bot.get_file(photo.file_id)
    # Скачиваем файл
    if isinstance(file, File):
        await bot.download_file(file.file_path, "/tmp/image.png")
    binary_data = open("/tmp/image.png", "rb").read()

    # проверяем наличие картинки в базе
    image = await Image.query.where(Image.file == binary_data).gino.first()
    if image is not None:
        mess = f"Эта картинка уже есть в базе\nid: {image.id}\nname: {image.name}"
        return await update_message(
            bot,
            message,
            mess.replace("_", "\\_"),
            add_keyboard({"назад": CallAny(action="start").pack()}),
            image_id=image.id,
        )

    # если картинки нет в баз, записываем ее в базу
    # и спрашиваем название у пользователя
    image = await Image.create(
        name="",
        file_id=photo.file_id,
        file=binary_data,
        u_id=user.id,
    )

    mess = f"Я запомнил картинку, ее id: \n {image.id}".replace("_", "\\_")

    DICT = {
        "добавить название": CallAny(
            action="ask_name_Image", user_id=user.id, image_id=image.id
        ).pack()
    }
    return await update_message(
        bot,
        message,
        mess.replace("_", "\\_"),
        add_keyboard(DICT),
        image_id=image.id,
    )
