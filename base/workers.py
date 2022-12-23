from .base import metadata

from sqlalchemy import Table, Column, Integer, String

t_workers = Table(
    "workers",
    metadata,
    Column('w_id', Integer),  # telegram id
    Column('name', String),  # фамилия
    Column('first_name', String),  # имя
    Column('mid_name', String),  # отчество
    Column('birthday', String),  # имя пользователя в телеге если есть
    Column('phone', String),  # является ли администратором
        )
