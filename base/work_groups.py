from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, ARRAY, String, DateTime

t_work_groups = Table(
    "work_groups",
    metadata,
    Column('g_id',        SmallInteger, primary_key=True),  # просто номер
    Column('name',        String),  # название группы
    Column('u_id',        SmallInteger),  # начальник группы
    Column('workers',     ARRAY(SmallInteger)),  # список подчинённых
    Column('date_update', DateTime),  # время обновления строки
        )
