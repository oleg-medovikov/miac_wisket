from pandas import DataFrame

from mdls import Struct, Image
from conf import db
from func import write_styling_excel


async def get_all_Struct() -> str:
    """Вытаскиваем все группы и возвращаем путь до файла"""

    DATA = (
        await db.select(
            [
                Struct.oid,
                Struct.image_id,
                Image.name,
                Struct.kind,
                Struct.name,
                Struct.short_name,
                Struct.level,
                Struct.active,
            ]
        )
        .select_from(Struct.outerjoin(Image))
        .order_by(Struct.oid)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "oid",
            "image_id",
            "image_name",
            "kind",
            "name",
            "short_name",
            "level",
            "active",
        ],
    )

    filename = "/tmp/Struct.xlsx"
    write_styling_excel(filename, df, "struct")
    return filename
