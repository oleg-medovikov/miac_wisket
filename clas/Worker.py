from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from base import database, t_workers


class Worker(BaseModel):
    w_id:       int
    name:       str
    first_name: str
    mid_name:   str
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
                'mid_name':   'Отчество',
                'birthday':   '2022-01-31',
                'phone':      '+7(931)777-77-77',
                'dateupdate': 'не заполнять'
                }]

    @staticmethod
    async def update(list_: list) -> str:
        "Обновление данных о сотрудниках"
        if len(list_) == 0:
            return 'Нечего обновлять'

        string = ''
        for worker in list_:
            query = t_workers.select(t_workers.c.w_id == worker['w_id'])
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил сотрудника {worker['w_id']}"
                worker['dateupdate'] = datetime.now()
                query = t_workers.insert().values(**worker)
                await database.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if worker[key] != value and key != 'dateupdate':
                    string += f"обновил сотрудника {worker['w_id']}"
                    worker['dateupdate'] = datetime.now()
                    query = t_workers.update()\
                        .where(t_workers.c.w_id == worker['w_id'])\
                        .values(**worker)
                    await database.execute(query)
        if string == '':
            string = 'Нечего обновлять'
        return string
