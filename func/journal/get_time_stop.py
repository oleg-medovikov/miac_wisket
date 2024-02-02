from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import Optional

from mdls import Worker, Journal
from conf import svup_sql


async def get_time_stop(date: Optional[datetime] = None):
    """
    Функция определяет время ухода воркеров с работы
     - достаем все id_svup всех воркеров,
     - достаем все события из базы данных с этими воркерами
     - диапозон времени с 17 00 даты до 4 00 след даты
       если текущее время с 0 до 7 - смотрим вчерашнюю дату
       если рассматриваемаемая дата не пустая
       игнорируем выход из функции по времени с 4 по 17
       (выход чтобы снять лишнюю нагрузку с базы)
     - по каждому воркеру вытаскиваем из журнала строку за сегодня
     - ищем время ухода в данных события и в случае успеха изменяем строку в журнале
     время ухода может продлеваться, поэтому вытаскиваем строчки, где уже есть время ухода
    """

    if date is None:
        if 4 < datetime.now().hour < 17:
            # Уходящих разглядываем с 5 вечера до 4 утра
            return
        if datetime.now().hour < 7:
            today = datetime.today() - timedelta(days=1)
            tomorrow = datetime.today()
        else:
            today = datetime.today()
            tomorrow = datetime.today() + timedelta(days=1)
    else:
        today = date
        tomorrow = date + timedelta(days=1)

    workers = await Worker.query.gino.all()

    # однострочник, который вытаскивает все id в одну строчку через запятую
    svup_ids = ", ".join(
        str(_.id_svup).replace("[", "").replace("]", "") for _ in workers
    )

    sql = f"""
SELECT HozOrgan as id_svup, max(TimeVal) as 'time_stop', min(TimeVal) as 'time_start'
    FROM [dbo].[pLogData]
    where  TimeVal between '{today.strftime('%Y%m%d')} 07:00:00' and '{tomorrow.strftime('%Y%m%d')} 04:00:00' 
        --and Event = 32
        and HozOrgan in ({svup_ids})
    GROUP BY HozOrgan
"""

    df = svup_sql(sql)

    for worker in workers:
        # берём строчку в журналёе
        journal = await Journal.query.where(
            and_(Journal.day == today, Journal.worker_id == worker.id)
        ).gino.first()

        # пытаемся вытащить время ухода
        try:
            time_stop = (
                df.loc[df.id_svup.isin(worker.id_svup), "time_stop"].max().time()
            )
        except (ValueError, AttributeError):
            if journal:
                continue
            await Journal.create(day=today, worker_id=worker.id)
            continue
        else:
            # если по каким-то причинам записи в журнале не было,
            # нужно ее создать, узнав дату прихода
            if journal is None:
                time_start = (
                    df.loc[df.id_svup.isin(worker.id_svup), "time_start"].min().time()
                )
                await Journal.create(
                    day=today,
                    worker_id=worker.id,
                    time_start=time_start,
                    time_stop=time_stop,
                )
            else:
                await journal.update(time_stop=time_stop).apply()
