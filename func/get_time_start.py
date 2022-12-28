from datetime import date, datetime

from clas import Worker, Journal
from base import svup_sql


async def get_time_start(scheduler: bool):
    "Получаем время прихода для всех сотрудников"

    # если функция запущена шедулером, то проверяем час
    if scheduler:
        if not (7 < datetime.now().hour < 17):
            return 1

    WORKERS = await Worker.get_all_id()

    DATE = date.today()

    sql = f"""
        SELECT HozOrgan as id_svup, min(TimeVal) as 'time_start'
            FROM [dbo].[pLogData]
                where  TimeVal > '{DATE.strftime('%Y%m%d')} 07:00:00'
                    and Event = 32
                    and HozOrgan in ({str(WORKERS)[1:-1]})
        GROUP BY HozOrgan
    """
    df = svup_sql(sql)

    WORKERS = await Worker.get_all()

    for worker in WORKERS:
        # создаём строку в журнале
        JOURNAL = await Journal.get(worker['w_id'], DATE)
        # если время прихода уже есть, то пропускаем
        if JOURNAL.time_start is not None:
            continue

        # пытаемся вытащить время прихода
        id_svup = [int(x) for x in worker['id_svup'][1:-1].split(',')]
        try:
            TIME = df.loc[
                df['id_svup'].isin(id_svup),
                'time_start'].min().time()
        except ValueError:
            continue
        else:
            JOURNAL.time_start = TIME
            await JOURNAL.update()
