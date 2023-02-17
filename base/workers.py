from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, ARRAY, String,\
    Date, DateTime

t_workers = Table(
    "workers",
    metadata,
    Column('w_id',        SmallInteger),  # просто номер
    Column('id_svup',     ARRAY(SmallInteger)),  # список номеров карт в охране
    Column('name',        String),  # фамилия
    Column('first_name',  String),  # имя
    Column('mid_name',    String),  # отчество
    Column('birthday',    Date),  # дата рождения
    Column('phone',       String),  # телефон
    Column('date_update', DateTime),  # время обновления строки
        )
