from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime

from mdls import User, Struct


async def read_Struct(user: User) -> str:
    df = read_excel(
        "/tmp/_Struct.xlsx", usecols=[_.name for _ in Struct.__table__.columns]
    )
    df.dropna(how="all", inplace=True)
    mess = ""
    for row in df.to_dict("records"):
        for key in ["image_id"]:
            if not isinstance(row[key], int):
                row[key] = None

        for key in ["active"]:
            if not isinstance(row[key], bool):
                row[key] = bool(row[key])

        for key in ["kind", "name", "short_name", "oid"]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            else:
                row[key] = ""

        # если есть идентичная строчка пропускаем
        object = await Struct.query.where(
            and_(*[getattr(Struct, k) == v for k, v in row.items()])
        ).gino.first()

        if object:
            continue
        # есть есть строчка с такимже id - апдейтим
        object = await Struct.query.where(Struct.oid == row["oid"]).gino.first()
        if object is not None:
            row["u_id"] = user.id
            row["date_update"] = datetime.now()
            await object.update(
                **{
                    key: value
                    for key, value in row.items()
                    if key in Struct.__table__.columns
                }
            ).apply()
            mess += f"\nОбновил строку: {row['oid']}"
            continue
        # или создаем новую строку
        row["u_id"] = user.id
        await Struct.create(
            **{
                key: value
                for key, value in row.items()
                if key in Struct.__table__.columns
            }
        )
        mess += f"\nДобавил строку: {row['oid']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
