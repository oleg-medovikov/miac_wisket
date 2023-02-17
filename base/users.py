from .base import metadata

from sqlalchemy import Table, Column, BigInteger, Integer, String, Boolean

t_users = Table(
    "users",
    metadata,
    Column('u_id',    BigInteger),  # telegram id
    Column('w_id',    Integer),  # id системы охраны
    Column('name',    String),  # фамилия c инициалами
    Column('name_tg', String),  # имя пользователя в телеге если есть
    Column('admin',   Boolean),  # является ли администратором
        )
