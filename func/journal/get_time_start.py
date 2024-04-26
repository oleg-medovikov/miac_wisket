from datetime import datetime
from sqlalchemy import and_
from typing import Optional

from mdls import Worker, Journal
from conf import svup_sql


async def get_time_start(date: Optional[datetime] = None):
    """
    Функция определяет время прихода воркеров на работу
     - если дата не пустая  игнорируем время выхода из функции
     - достаем все id_svup всех воркеров,
     - достаем все события из базы данных с этими воркерами
     - по каждому воркеру вытаскиваем из журнала строку за сегодня
     - ищем время прихода в данных события и в случае успеха создаем строку в журнале
    """

    if date is None:
        if not (7 < datetime.now().hour < 17):
            # функция работает с 7 утра до 17 вечера
            return
        today = datetime.today()
    else:
        today = date

    start = today.replace(hour=7)
    stop = today.replace(hour=23)

    start_int = int((start - datetime(1970, 1, 1)).total_seconds())
    stop_int = int((stop - datetime(1970, 1, 1)).total_seconds())

    workers = await Worker.query.gino.all()

    # однострочник, который вытаскивает все id в одну строчку через запятую
    svup_ids = ", ".join(
        str(_.id_svup).replace("[", "").replace("]", "") for _ in workers
    )

    sql = f"""
SELECT HozOrgan as id_svup, min(TimeVal) as 'time_start'
    FROM [dbo].[pLogData]
        where DATEDIFF(second, '1970-01-01', TimeVal) between {start_int} and {stop_int}
            -- and Event = 32
            and HozOrgan in ({svup_ids})
    GROUP BY HozOrgan
"""

    df = svup_sql(sql)

    for worker in workers:
        journal = await Journal.query.where(
            and_(Journal.day == today, Journal.worker_id == worker.id)
        ).gino.first()

        if journal is not None and journal.time_start is not None:
            continue

        try:
            time = df.loc[df.id_svup.isin(worker.id_svup), "time_start"].min().time()
        except (ValueError, AttributeError):
            continue
        else:
            if journal:
                await journal.update(time_start=time).apply()
            else:
                await Journal.create(day=today, worker_id=worker.id, time_start=time)
