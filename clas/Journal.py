from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_

from datetime import date, time

from base import database, t_journal


class Journal(BaseModel):
    day:        date
    w_id:       int
    time_start: Optional[time]
    time_stop:  Optional[time]
    time_lose:  Optional[int]
    time_win:   Optional[int]
    status_id:  Optional[int]
    w_comment:  Optional[str]

    @staticmethod
    async def get(w_id: int, date: 'date') -> 'Journal':
        query = t_journal.select(and_(
            t_journal.c.day == date,
            t_journal.c.w_id == w_id))
        res = await database.fetch_one(query)
        if res is None:
            Dict = {
                'day': date,
                'w_id': w_id,
                    }
            query = t_journal.insert().values(**Dict)
            await database.execute(query)
            return Journal(**Dict)
        else:
            return Journal(**res)

    async def add(self):
        """Просто добавить строчку в таблицу,
        если уже есть, то ничего не делать"""
        query = t_journal.select(and_(
            t_journal.c.day == self.day,
            t_journal.c.w_id == self.w_id))
        res = await database.fetch_one(query)
        if res is None:
            query = t_journal.insert().values(self.dict())
            await database.execute(query)

    async def update(self):
        "Обновить строку, если нет, то добавить"
        query = t_journal.select(and_(
            t_journal.c.day == self.day,
            t_journal.c.w_id == self.w_id))
        res = await database.fetch_one(query)
        if res is None:
            query = t_journal.insert().values(self.dict())
            await database.execute(query)
        else:
            query = t_journal.update()\
                .where(and_(
                    t_journal.c.day == self.day,
                    t_journal.c.w_id == self.w_id))\
                .values(self.dict())
            await database.execute(query)

    @staticmethod
    async def get_journal(WORKERS: list, START: 'date', STOP: 'date') -> list:
        "Получаем журнал с событиями"
        pass


