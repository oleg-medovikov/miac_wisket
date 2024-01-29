from conf import db
from mdls import Journal
from sqlalchemy import func

names = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


async def get_months():
    """Получаем список доступных в журнале месяцев"""

    query = (
        db.select(
            [
                func.extract("year", Journal.day).label("year"),
                func.extract("month", Journal.day).label("month"),
            ]
        )
        .group_by(func.extract("year", Journal.day), func.extract("month", Journal.day))
        .order_by(
            func.extract("year", Journal.day).desc(),
            func.extract("month", Journal.day).desc(),
        )
    )

    # Выполняем запрос и получаем результаты
    results = await query.gino.all()
    results = [(int(a), int(b)) for a, b in results if a is not None and b is not None]
    # Преобразуем результаты в список словарей
    return [
        {
            "year": year,
            "month": month,
            "name": names.get(month),
        }
        for year, month in results
    ]
