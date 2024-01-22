import sqlalchemy
from sqlalchemy.exc import OperationalError
import pandas as pd
import logging

from conf.config import settings


def svup_sql(sql):
    "Делаем запросы к базе охраны"
    try:
        engine = sqlalchemy.create_engine(settings.SVUP_SQL)
        connection = engine.raw_connection()
        return pd.read_sql(sql, connection)
    except OperationalError as e:
        logging.error(f"!!!Нет доступа к базе {settings.SVUP_SQL}\n{str(e)}")
        return pd.DataFrame()
