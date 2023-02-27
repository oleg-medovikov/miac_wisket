from .dispetcher import dp
from aiogram import types
import os

from clas import User
from func import delete_message
from base import svup_sql
from func import write_styling_excel_file

sql = """select
    person.Name as fio, event.TimeVal, event.Remark
        from
            (SELECT * from [dbo].[pLogData]
                where Event = 32
                and TimeVal > '20230221') as event
        inner join dbo.pList as  person
            on(event.HozOrgan = person.id)
        where person.Name in( 'Шарин', 'Медовиков')"""


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        await message.answer("неизвестный юзер", parse_mode='html')

    MESS = f'добрый день, {USER.name}!'

    try:
        df = svup_sql(sql)
    except Exception as e:
        await message.answer(str(e), parse_mode='html')

    file = 'temp/sql.xlsx'

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    await message.answer(MESS, parse_mode='html')
    os.remove(file)
