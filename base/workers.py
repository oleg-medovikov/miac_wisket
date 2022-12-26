from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Date, DateTime

t_workers = Table(
    "workers",
    metadata,
    Column('w_id', Integer),  # telegram id
    Column('name', String),  # фамилия
    Column('first_name', String),  # имя
    Column('mid_name', String),  # отчество
    Column('birthday', Date),  # дата рождения
    Column('phone', String),  # телефон
    Column('dateupdate', DateTime),  # время обновления строки
        )
