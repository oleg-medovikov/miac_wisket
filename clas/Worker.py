from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from base import database, t_workers


class Worker(BaseModel):
    w_id:       int
    name:       str
    first_name: str
    mid_mame:   str
    birthday:   Optional[date]
    phone:      str
    dateupdate: datetime

    @staticmethod
    async def get(w_id: int) -> Optional['Worker']:
        query = t_workers.select(t_workers.c.w_id == w_id)
        res = await database.fetch_one(query)
        if res is not None:
            return Worker(**res)

    @staticmethod
    async def get_all() -> list:
        query = t_workers.select().order_by(t_workers.c.w_id)
        res = await database.fetch_all(query)
        if len(res):
            list_ = []
            for row in res:
                list_.append(Worker(**row).dict())
            return list_
        else:
            return [{
                'w_id':       0,
                'name':       'Фамилия',
                'first_name': 'Имя',
                'mid_mame':   'Отчество',
                'birthday':   '2022-01-31',
                'phone':      '+7(931)777-77-77',
                'dateupdate': 'не заполнять'
                }]
