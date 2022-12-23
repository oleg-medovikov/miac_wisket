from .base import metadata

from sqlalchemy import Table, Column, Integer, Date, Datetime

t_journal = Table(
    "journal",
    metadata,
    Column('day', Date),  # день
    Column('w_id', Integer),  # id сотрудника
    Column('time_start', Datetime),  # время прихода на работу
    Column('time_stop', Datetime),  # время ухода с работы
    Column('time_lose', Integer),  # время отсутствия в минутах
    Column('time_win', Integer),  # время переработки в минутах
    Column('status_id', Integer),  # статус, объясняющий отсутствие
    )
