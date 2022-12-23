from databases import Database
from sqlalchemy import create_engine, MetaData

from conf import DATABASE_POSTGRESS

database = Database(DATABASE_POSTGRESS)
metadata = MetaData()
engine = create_engine(DATABASE_POSTGRESS)
