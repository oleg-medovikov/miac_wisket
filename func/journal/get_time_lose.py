from datetime import datetime
from sqlalchemy import and_, null
import logging

from mdls import Worker, Journal
from conf import svup_sql


async def get_time_lose():
    """
    Функция определяет время, насколько воркер покинул здание
        - достаем все записи журнала с пустым time_lose и закрытым time_stop
        - по очереди вытаскиваем данные из базы
        - если вытаскиваем пустоту, то воркер не выходил из здания
        - обновляем запись в журнале
    """

    journals = (
        await Journal.load(worker=Worker)
        .query.where(
            and_(
                Journal.time_start != null(),
                Journal.time_stop != null(),
                Journal.time_lose == null(),
                Journal.day < datetime.today(),
            )
        )
        .gino.all()
    )

    for journal in journals:
        svup_ids = ", ".join(map(str, journal.worker.id_svup))
        day = journal.day.strftime("%Y%m%d")

        sql = f"""
SELECT
	subtable.HozOrgan
	,sum(subtable.LunchTimeInMinutes) as AllLoseTime
FROM(
	SELECT 
		e.HozOrgan,
		CONVERT(VARCHAR(5), CAST(e.TimeVal AS TIME), 108) as Time,
		DATEDIFF(MINUTE, e.TimeVal, MIN(l.TimeVal)) AS LunchTimeInMinutes
	FROM
		dbo.pLogData e
	JOIN
		dbo.pLogData l ON e.HozOrgan = l.HozOrgan AND e.TimeVal < l.TimeVal 
	WHERE
		e.Remark LIKE '%Выход%'
		-- and l.Remark LIKE '%Вход%' 
		and e.TimeVal between '{day} 09:00:00' and '{day} 17:30:00'
		and l.TimeVal between '{day} 09:00:00' and '{day} 17:30:00'
		and e.Event = 32
		and l.Event = 32
		and e.HozOrgan in ({svup_ids})
	GROUP BY
		e.HozOrgan, e.TimeVal ) as subtable
GROUP BY
	subtable.HozOrgan
ORDER BY
	subtable.HozOrgan
"""
        df = svup_sql(sql)
        if len(df) == 0:
            await journal.update(time_lose=0).apply()
            continue
        await journal.update(time_lose=df["AllLoseTime"].sum()).apply()
