from .dispetcher import dp
from aiogram import types
from datetime import datetime

from clas import User, Worker, Journal
from func import delete_message
from base import svup_sql


@dp.message_handler(commands='journal')
async def get_journal_commands(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    MESS = """*Доступные команды для ведения журнала:*

    *Записать время прихода*
        /journal_time_start
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')


@dp.message_handler(commands=['journal_time_start'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    WORKERS = await Worker.get_all_id()
    DATE = datetime.now().strftime('%Y%m%d')

    sql = f"""
        SELECT HozOrgan as w_id, min(TimeVal) as 'time_start'
            FROM [dbo].[pLogData]
                where  TimeVal > '{DATE} 07:00:00'
                    and Event = 32
                    and HozOrgan in ({str(WORKERS)[1:-1]})
        GROUP BY HozOrgan
    """

    df = svup_sql(sql)

    for worker in WORKERS:
        JOURNAL = await Journal.get(worker)
        if worker in df['w_id'].unique() and JOURNAL.time_start is None:
            TIME = df.loc[
                df['w_id'] == worker,
                'time_start'
                ].dt.time.values[0]

            JOURNAL.time_start = TIME
            await JOURNAL.update()

    return await message.answer('Done', parse_mode='Markdown')
