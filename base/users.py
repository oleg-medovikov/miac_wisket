from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean

t_users = Table(
    "users",
    metadata,
    Column('u_id', String),  # telegram id
    Column('sec_id', Integer),  # id системы охраны
    Column('name', String),  # фамилия
    Column('first_name', String),  # имя
    Column('mid_name', String),  # отчество
    Column('name_tg', String),  # имя пользователя в телеге если есть
    Column('admin', Boolean),  # является ли администратором
        )
