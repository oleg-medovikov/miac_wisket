from .dispetcher import dp
from aiogram import types
import os

from clas import Work_Group, Worker_Day
from func import delete_message, write_styling_excel_file, \
    create_tabel

from datetime import datetime, date
from calendar import monthrange


def return_mounth(DATE) -> tuple['date', 'date']:
    "Получение дат начала и конца текущего месяца"
    # количество дней в месяце
    days = monthrange(DATE.year, DATE.month)[1]
    return date(DATE.year, DATE.month, 1), date(DATE.year, DATE.month, days)


@dp.message_handler(commands='tabel')
async def get_tabel_file(message: types.Message):
    await delete_message(message)

    WG = await Work_Group.get(message['from']['id'])
    START, STOP = return_mounth(datetime.today())

    WDS = await Worker_Day.get_journal(WG.workers, START, STOP)
    df = create_tabel(WDS)

    file = 'temp/табель.xlsx'
    write_styling_excel_file(file, df, WG.name, True)
    await message.answer_document(open(file, 'rb'))
    os.remove(file)
