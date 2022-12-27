from .dispetcher import dp
from aiogram import types
import os

from clas import User
from func import delete_message
from base import svup_sql
from func import write_styling_excel_file


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None

    MESS = f'добрый день, {USER.name}!'
    await message.answer(MESS, parse_mode='html')


async def procedure(message):

    sql = """select person.Name +' '+ person.FirstName +' '+ person.MidName as fio, Time,
    remark
    from(
    SELECT cast(TimeVal as time) as Time, HozOrgan, Remark
      FROM [dbo].[pLogData]
      where cast(TimeVal as date) = cast(getdate() as date)
      and Event = 32 ) as event
      inner join dbo.pList as  person
      on(event.HozOrgan = person.id)
      where person.Name = 'Шарин'
      order by Time Desc"""

    sql = """
    select person.Name as fio, event.TimeVal, event.Remark
    from
    (SELECT * from [dbo].[pLogData]
    where Event = 32
    and TimeVal > '20221101') as event
    inner join dbo.pList as  person
    on(event.HozOrgan = person.id)
    where person.Name in( 'Шарин', 'Медовиков')
    """
    df = svup_sql(sql)

    file = 'temp/sql.xlsx'

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    os.remove(file)
