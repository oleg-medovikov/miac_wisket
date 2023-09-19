from pydantic import BaseModel

from base import database, t_choice


class Choice(BaseModel):
    u_id:       int
    w_id:       int

    @staticmethod
    async def add(U_ID: int, W_ID: int):
        query = t_choice.delete().where(
            t_choice.c.u_id == U_ID
            )
        await database.execute(query)
        query = t_choice.insert().values(
                {
                    'u_id': U_ID,
                    'w_id': W_ID,
                }
            )
        await database.execute(query)

    @staticmethod
    async def get_worker(U_ID: int) -> int:
        query = t_choice.select(t_choice.c.u_id == U_ID)
        res = await database.fetch_one(query)
        return res['w_id']
