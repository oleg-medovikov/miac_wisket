from disp.admin import router
from aiogram import F, Bot
from aiogram.types import Message
import re
import pandas as pd
import logging

from func import delete_message, update_message, add_keyboard, get_time_stop
from mdls import User
from conf import CallAny


@router.message(F.text.startswith("journal"))
async def journal_mount(message: Message, bot: Bot):
    """когда админ хочет заполнить журнал за месяц"""
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    dict_ = {"назад": CallAny(action="start").pack()}

    # вытаскиваем дату из сообщения
    pattern = r"(\d{4})\.(\d{2})"
    match = re.search(pattern, str(message.text))
    if match:
        year = match.group(1)
        month = match.group(2)
        logging.info(f"!!!год: {year} месяц: {month}")
    else:
        mess = "в сообщении должен быть номер месяца в виде 'journal 2024.01'"
        return await update_message(
            bot, message, mess, add_keyboard(dict_), image_name="admin"
        )

    # Определяем количество дней в месяце
    num_days = pd.Period(f"{year}-{month}").days_in_month
    # Создаем ряд дат для заданного месяца и года
    dates = pd.date_range(start=f"{year}-{month}-01", periods=num_days, freq="D")

    for date in dates:
        logging.info(f"!!! Узнаю время ухода для даты {date.strftime('%d-%m-%Y')}")
        await get_time_stop(date)
        logging.info("!!! Успех")

    mess = f"Я закончил с {month} месяцем!"
    return await update_message(
        bot, message, mess, add_keyboard(dict_), image_name="admin"
    )
