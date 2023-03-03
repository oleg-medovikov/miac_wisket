from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, ARRAY, String,\
    Date, DateTime

t_workers = Table(
    "workers",
    metadata,
    Column('w_id',        SmallInteger, primary_key=True),  # просто номер
    Column('id_svup',     ARRAY(SmallInteger)),  # список номеров карт в охране
    Column('name',        String),  # фамилия
    Column('first_name',  String),  # имя
    Column('mid_name',    String),  # отчество
    Column('birthday',    Date, nullable=True, default=None),  # дата рождения
    Column('phone',       String, nullable=True, default=None),  # телефон
    Column('date_update', DateTime),  # время обновления строки
        )
