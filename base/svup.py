import pandas as pd
import sqlalchemy

from conf import DATABASE_SVUP


def svup_sql(sql):
    "Делаем запросы к базу ковид"
    with sqlalchemy.create_engine(
            DATABASE_SVUP,
            pool_pre_ping=True).connect() as con:
        return pd.read_sql(sql, con)
