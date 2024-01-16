from pandas import DataFrame

from mdls import Struct, Image
from conf import db


async def get_all_Struct() -> str:
    """Вытаскиваем все группы и возвращаем путь до файла"""

    DATA = (
        await db.select(
            [
                Struct.id,
                Struct.oid,
                Struct.image_id,
                Image.name,
                Struct.type,
                Struct.name,
                Struct.short_name,
                Struct.level,
                Struct.active,
            ]
        )
        .select_from(Struct.outerjoin(Image))
        .order_by(Struct.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "oid",
            "image_id",
            "image_name",
            "type",
            "name",
            "short_name",
            "level",
            "active",
        ],
    )

    filename = "/tmp/Struct.xlsx"
    df.to_excel(filename, index=False)
    return filename
