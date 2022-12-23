from .base import metadata

from sqlalchemy import Table, Column, Integer, Datetime

t_subordination = Table(
    "subordination",
    metadata,
    Column('w_id_boss', Integer),
    Column('w_id', Integer),
    Column('updatetime', Datetime),
    )
