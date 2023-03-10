from datetime import datetime, timedelta, date

from clas import Worker, Journal
from base import svup_sql


async def get_time_stop(scheduler: bool):
    "Получаем время прихода для всех сотрудников"

    # если функция запущена шедулером, то проверяем час
    if scheduler:
        if (4 < datetime.now().hour < 17):
            return 1

    WORKERS = await Worker.get_all_id()

    if datetime.now().hour < 7:
        DATE = date.today() - timedelta(days=1)
    else:
        DATE = date.today()

    sql = f"""
        SELECT HozOrgan as id_svup, max(TimeVal) as 'time_stop'
            FROM [dbo].[pLogData]
                where  TimeVal > '{DATE.strftime('%Y%m%d')} 07:00:00'
                    and Event = 32
                    and HozOrgan in ({str(WORKERS)[1:-1]})
        GROUP BY HozOrgan
    """
    df = svup_sql(sql)

    WORKERS = await Worker.get_all()

    for worker in WORKERS:
        # берём строчку в журнале
        JOURNAL = await Journal.get(worker['w_id'], DATE)

        # пытаемся вытащить время ухода
        id_svup = [int(x) for x in worker['id_svup']]
        try:
            TIME = df.loc[
                df['id_svup'].isin(id_svup),
                'time_stop'].max().time()
        except ValueError:
            continue
        else:
            JOURNAL.time_stop = TIME
            await JOURNAL.update()


async def get_time_stop_mounth():
    "Получаем время ухода для всех сотрудников за месяц"
    WORKERS = await Worker.get_all_id()

    DATE = date(date.today().year, date.today().month, 1)
    sql = f"""
        SELECT HozOrgan as id_svup,
            cast(TimeVal as date) as day, max(TimeVal) as 'time_stop'
            FROM [dbo].[pLogData]
            where  TimeVal >= '{DATE.strftime('%Y%m%d')} 07:00:00'
            and TimeVal < '{date.today().strftime('%Y%m%d')} 00:00:01'
            and HozOrgan in ({str(WORKERS)[1:-1]})
        GROUP BY HozOrgan, cast(TimeVal as date)
    """
    df = svup_sql(sql)
    WORKERS = await Worker.get_all()

    for worker in WORKERS:
        # создаём строку в журнале
        for DAY in df['day'].unique():
            JOURNAL = await Journal.get(worker['w_id'], DAY)
            if JOURNAL.time_stop is not None:
                continue

            # пытаемся вытащить время ухода
            id_svup = [int(x) for x in worker['id_svup']]
            try:
                TIME = df.loc[
                    (df['id_svup'].isin(id_svup)) & (df['day'] == DAY),
                    'time_stop'].max().time()
            except ValueError:
                continue
            else:
                JOURNAL.time_stop = TIME
                await JOURNAL.update()
