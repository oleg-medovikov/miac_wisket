from .dispetcher import dp
from aiogram import types
from datetime import datetime
import os
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from clas import User, Worker, Choice
from func import delete_message, write_styling_excel_file, to_rus
from base import svup_sql


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_workers_day(message: types.Message):
    await delete_message(message)
    USER = await User.get(message['from']['id'])
    if USER is None:
        return await message.answer("неизвестный юзер", parse_mode='html')

    NAME = to_rus(message.text).title()

    try:
        WORKER = await Worker.find(NAME)
    except ValueError:
        MESS = f'добрый день, {USER.name}.' \
            + f'\n Я не нашел рабочего {NAME}'
        await message.answer(MESS, parse_mode='html')
    else:
        await Choice.add(USER.u_id, WORKER.w_id)

        await message.answer(
                text=f"Выбор даты для {NAME}:",
                reply_markup=await SimpleCalendar().start_calendar(
                    datetime.now().year,
                    datetime.now().month
                    ))


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(
        callback_query: types.CallbackQuery,
        callback_data: dict):

    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
        )

    if selected:
        U_ID = callback_query['from']['id']
        W_ID = await Choice.get_worker(U_ID)
        WORKER = await Worker.get(W_ID)

        sql = f"""select
            person.Name as fio, event.TimeVal, event.Remark
                from
                    (SELECT * from [dbo].[pLogData]
                        where Event = 32
                        and cast(TimeVal as date) = '{date.strftime('%Y%m%d')}'
                        ) as event
                inner join dbo.pList as  person
                    on(event.HozOrgan = person.id)
                where person.id in({str(WORKER.id_svup)[1:-1]})"""

        try:
            df = svup_sql(sql)
        except Exception as e:
            await callback_query.message.answer(str(e), parse_mode='html')

        file = f'temp/{WORKER.name} за {date.strftime("%d-%m-%Y")}.xlsx'

        write_styling_excel_file(file, df, 'svod')
        await callback_query.message.answer_document(open(file, 'rb'))
        os.remove(file)
