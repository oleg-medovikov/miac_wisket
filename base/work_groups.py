from .base import metadata

from sqlalchemy import Table, Column, BigInteger, SmallInteger, \
    ARRAY, String, DateTime

t_work_groups = Table(
    "work_groups",
    metadata,
    Column('u_id',        BigInteger, primary_key=True),  # начальник группы
    Column('name',        String),  # название группы
    Column('workers',     ARRAY(SmallInteger)),  # список подчинённых
    Column('date_update', DateTime),  # время обновления строки
        )
