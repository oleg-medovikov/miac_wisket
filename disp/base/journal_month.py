from disp.base import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, get_months
from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "journal_month"))
async def journal_month(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут вытаскиваются все доступные месяца и предлагаем на выбор первые 6
    """
    months = await get_months()
    DICT = {}
    callback_data.action = "journal_get"
    for month in months[:6]:
        callback_data.year = month["year"]
        callback_data.month = month["month"]
        DICT[month["name"] + f' {month["year"]}'] = callback_data.pack()

    mess = "Выберите доступный месяц для журнала"
    await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT),
        True,
        image_name="calendar",
    )
