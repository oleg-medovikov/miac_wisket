from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Datetime

# пока хз, что делать с это таблицей
# пока не нужна

t_devisions = Table(
    "devisions",
    metadata,
    Column('d_id', Integer),  # id отдела
    Column('d_id', Integer),  #
    )
