from pandas import read_excel
from pandas._libs.tslibs.timestamps import Timestamp
from sqlalchemy import and_
from datetime import datetime
from ast import literal_eval

from mdls import User, Worker


async def read_Worker(user: User) -> str:
    df = read_excel(
        "/tmp/_Worker.xlsx",
        usecols=[
            _.name for _ in Worker.__table__.columns if _.name not in ["date_update"]
        ],
    )

    df.dropna(how="all", inplace=True)

    mess = ""
    for row in df.to_dict("records"):
        for key in ["image_id"]:
            if not isinstance(row[key], int):
                row[key] = None

        for key in ["id_svup"]:
            if isinstance(row[key], str):
                row[key] = [int(_) for _ in literal_eval(row[key])]

        for key in ["name", "first_name", "oid", "mid_name", "phone"]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            elif isinstance(row[key], int):
                row[key] = str(row[key])
            elif isinstance(row[key], float):
                try:
                    row[key] = str(int(row[key]))
                except ValueError:
                    row[key] = ""
            else:
                row[key] = ""

        for key in ["birthday"]:
            if isinstance(row[key], str):
                try:
                    row[key] = datetime.strptime(row[key], "%d.%m.%Y").date()
                except:
                    row[key] = None
            elif isinstance(row[key], Timestamp):
                row[key] = row[key].date()
            else:
                row[key] = None

        # если есть идентичная строчка пропускаем
        object = await Worker.query.where(
            and_(*[getattr(Worker, k) == v for k, v in row.items()])
        ).gino.first()

        if object:
            continue
        # есть есть строчка с таким же id - апдейтим
        object = await Worker.query.where(Worker.id == row["id"]).gino.first()

        row["u_id"] = user.id
        row["date_update"] = datetime.now()

        if object is not None:
            await object.update(
                **{
                    key: value
                    for key, value in row.items()
                    if key in Worker.__table__.columns
                }
            ).apply()
            mess += f"\nОбновил строку: {row['name']}"
            continue
        # или создаем новую строку
        await Worker.create(
            **{
                key: value
                for key, value in row.items()
                if key in Worker.__table__.columns
            }
        )
        mess += f"\nДобавил строку: {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
