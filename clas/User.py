from pydantic import BaseModel
from typing import Optional

from base import database, t_users


class User(BaseModel):
    u_id:       int
    w_id:       int
    name:       str
    name_tg:    str
    admin:      bool

    @staticmethod
    async def get(u_id: str) -> Optional['User']:
        "получение пользователя по телеграм id"
        query = t_users.select(t_users.c.u_id == u_id)
        res = await database.fetch_one(query)

        if res is not None:
            return User(**res)

    @staticmethod
    async def get_all() -> list:
        query = t_users.select().order_by(t_users.c.w_id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(User(**row).dict())
        return list_

    async def update(self):
        "Обновление данных о пользователе"
        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await database.fetch_one(query)

        if res is not None:
            pass
