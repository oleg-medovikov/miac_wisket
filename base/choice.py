from .base import metadata

from sqlalchemy import Table, Column, BigInteger, Integer

t_choice = Table(
    "choice",
    metadata,
    Column('u_id', BigInteger),  # telegram id
    Column('w_id', Integer),
        )
