from pydantic import BaseModel
from datetime import datetime
from json import loads

from base import database, t_work_groups


class Work_Group(BaseModel):
    u_id:       int
    name:       str
    workers:    list
    date_update: datetime

    @staticmethod
    async def get_workers(U_ID: int) -> list:
        "Получить список подчинённых у пользователя"
        query = t_work_groups.select(
            t_work_groups.c.u_id == U_ID
                )
        res = await database.fetch_one(query)
        if res is not None:
            return res['workers']
        else:
            return []

    @staticmethod
    async def get(U_ID: int) -> 'Work_Group':
        query = t_work_groups.select(
            t_work_groups.c.u_id == U_ID
                )
        res = await database.fetch_one(query)
        if res is not None:
            return Work_Group(**res)
        else:
            raise ValueError('У вас нет рабочей группы!')

    @staticmethod
    async def get_all() -> list:
        query = t_work_groups.select().order_by(
            t_work_groups.c.u_id
                )
        res = await database.fetch_all(query)
        if len(res):
            list_ = []
            for row in res:
                list_.append(Work_Group(**row).dict())
            return list_
        else:
            return [{
                'u_id':       0,
                'name':       'команда SOS',
                'workers':    '[]',
                'date_update': 'не заполнять'
                }]

    @staticmethod
    async def update(list_: list) -> str:
        "Обновление данных о рабочих группах"
        if len(list_) == 0:
            return 'Нечего обновлять'

        string = ''
        for row in list_:
            query = t_work_groups.select(
                t_work_groups.c.г_id == row['u_id'])

            res = await database.fetch_one(query)

            row['workers'] = loads(row['workers'])
            # если строки нет, то добавляем
            if res is None:
                string += f"\nдобавил группу {row['name']}"
                row['date_update'] = datetime.now()

                query = t_work_groups.insert().values(**row)
                await database.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"\nобновил группу {row['name']}"
                    row['date_update'] = datetime.now()
                    query = t_work_groups.update()\
                        .where(t_work_groups.c.u_id == row['u_id'])\
                        .values(**row)
                    await database.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
