from .base import database, engine, metadata
from .users import t_users
from .journal import t_journal
from .workers import t_workers

metadata.create_all(engine)
