from pandas import DataFrame
from datetime import datetime
from calendar import monthrange


def return_mounth(DATE: 'datetime'):
    "Получение дат начала и конца текущего месяца"
    days = monthrange(DATE.year, DATE.month)[1]
    return f'{DATE.year}-{DATE.month}-1', f'{DATE.year}-{DATE.month}-{days}'


def create_tabel(WORKERS: list) -> 'DataFrame':
    df = DataFrame()

    return df
