from .base import database, engine, metadata
from .users import t_users
from .journal import t_journal
from .workers import t_workers

from .svup import svup_sql
metadata.create_all(engine)
