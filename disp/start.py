from .dispetcher import dp
from aiogram import types
import os
from datetime import datetime

from clas import User, Worker
from func import delete_message
from base import svup_sql
from func import write_styling_excel_file

sql = f"""select
    person.Name as fio, event.TimeVal, event.Remark
        from
            (SELECT * from [dbo].[pLogData]
                where Event = 32
                and TimeVal >= '{datetime.now().strftime('%Y%m%d')}'
                ) as event
        inner join dbo.pList as  person
            on(event.HozOrgan = person.id)
        where person.id in(ID)"""


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return await message.answer("неизвестный юзер", parse_mode='html')

    WORKER = await Worker.get(USER.w_id)
    if WORKER is None:
        return await message.answer("неизвестный работник", parse_mode='html')

    MESS = f'добрый день, {USER.name}!'
    await message.answer(MESS, parse_mode='html')

    global sql
    sql = sql.replace('ID', str(WORKER.id_svup)[1:-1])

    try:
        df = svup_sql(sql)
    except Exception as e:
        await message.answer(str(e), parse_mode='html')

    file = 'temp/Ваши похождения за сегодня.xlsx'

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    os.remove(file)
