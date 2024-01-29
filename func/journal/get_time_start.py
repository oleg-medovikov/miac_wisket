from datetime import datetime
from sqlalchemy import and_, null
from typing import Optional

from mdls import Worker, Journal
from conf import svup_sql


async def get_time_start(date: Optional[datetime]):
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

    workers = await Worker.query.gino.all()

    # однострочник, который вытаскивает все id в одну строчку через запятую
    svup_ids = ", ".join(
        str(_.id_svup).replace("[", "").replace("]", "") for _ in workers
    )

    sql = f"""
SELECT HozOrgan as id_svup, min(TimeVal) as 'time_start'
    FROM [dbo].[pLogData]
        where  TimeVal between '{today.strftime('%Y%m%d')} 07:00:00' and '{today.strftime('%Y%m%d')} 23:00:00'
            -- and Event = 32
            and HozOrgan in ({svup_ids})
    GROUP BY HozOrgan
"""

    df = svup_sql(sql)

    for worker in workers:
        journal = await Journal.query.where(
            and_(
                Journal.day == date,
                Journal.worker_id == worker.id,
                Journal.time_start != null(),
            )
        ).gino.first()

        if journal:
            continue
        try:
            time = df.loc[df.id_svup.isin(worker.id_svup), "time_start"].min().time()
        except ValueError:
            continue
        else:
            await Journal.create(day=date, worker_id=worker.id, time_start=time)
