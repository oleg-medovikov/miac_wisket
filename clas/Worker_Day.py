from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_, select

from datetime import date, time

from base import database, t_journal, t_workers


class Worker_Day(BaseModel):
    day:        date
    w_id:       int
    fio:        str
    time_start: Optional[time]
    time_stop:  Optional[time]
    time_lose:  Optional[int]
    time_win:   Optional[int]
    status_id:  Optional[int]
    w_comment:  Optional[str]

    @staticmethod
    async def get_journal(WORKERS: list, START: 'date', STOP: 'date') -> list:
        "Получаем журнал с событиями"
        j = t_journal.join(
            t_workers,
            t_journal.c.w_id == t_workers.c.w_id
                )
        query = select([
            t_journal.c.day,
            t_journal.c.w_id,
            t_workers.c.name,
            t_workers.c.first_name,
            t_workers.c.mid_name,
            t_journal.c.time_start,
            t_journal.c.time_stop,
            t_journal.c.time_lose,
            t_journal.c.time_win,
            t_journal.c.status_id,
            t_journal.c.w_comment,
            ]).where(and_(
                t_journal.c.day >= START,
                t_journal.c.day <= STOP,
                t_journal.c.w_id.on_(WORKERS)
                )).select_from(j)

        list_ = []
        for row in await database.fetch_all(query):
            list_.append(Worker_Day(**row))
            return list_
