from pydantic import BaseModel
from typing import Optional

from base import database, t_users


class User(BaseModel):
    u_id:       str
    sec_id:     int
    name:       str
    first_name: str
    mid_name:   str
    name_tg:    str
    admin:      bool

    @staticmethod
    async def get(u_id: str) -> Optional['User']:
        "получение пользователя по телеграм id"
        query = t_users.select(t_users.c.u_id == str(u_id))
        res = await database.fetch_one(query)

        if res is not None:
            return User(**res)


    async def update(self):
        "Обновление данных о пользователе"
        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await database.fetch_one(query)

        if res is not None:
            pass
