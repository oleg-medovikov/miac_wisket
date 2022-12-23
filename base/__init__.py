from .base import database, engine, metadata
from .users import t_users


metadata.create_all(engine)
