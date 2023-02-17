from pydantic import BaseModel

from base import database, t_users


class User(BaseModel):
    u_id:       int
    w_id:       int
    name:       str
    name_tg:    str
    admin:      bool

    @staticmethod
    async def get(u_id: str) -> 'User':
        "получение пользователя по телеграм id"
        query = t_users.select(t_users.c.u_id == u_id)
        res = await database.fetch_one(query)

        if res is not None:
            return User(**res)
        else:
            raise ValueError('Нет такого пользователя!')

    @staticmethod
    async def get_all() -> list:
        "Получение списка пользователей"
        query = t_users.select().order_by(t_users.c.w_id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(User(**row).dict())
        return list_

    @staticmethod
    async def update(list_: list) -> str:
        "Обновление данных о пользователе"
        if len(list_) == 0:
            return 'Нечего обновлять'

        string = ''
        for user in list_:
            query = t_users.select(t_users.c.u_id == user['u_id'])
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил пользователя {user['u_id']}"
                query = t_users.insert().values(**user)
                await database.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if user[key] != value:
                    string += f"обновил пользователя {user['u_id']}"
                    query = t_users.update()\
                        .where(t_users.c.u_id == user['u_id'])\
                        .values(**user)
                    await database.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
