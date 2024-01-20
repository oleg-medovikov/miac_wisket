from pandas import DataFrame

from mdls import Worker, Image
from conf import db
from func import write_styling_excel


async def get_all_Worker() -> str:
    """Вытаскиваем всех пользователей и возвращаем путь до файла"""

    DATA = (
        await db.select(
            [
                Worker.id,
                Worker.oid,
                Worker.image_id,
                Image.name,
                Worker.id_svup,
                Worker.name,
                Worker.first_name,
                Worker.mid_name,
                Worker.birthday,
                Worker.phone,
            ]
        )
        .select_from(Worker.outerjoin(Image))
        .order_by(Worker.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "oid",
            "image_id",
            "image_name",
            "id_svup",
            "name",
            "first_name",
            "mid_name",
            "birthday",
            "phone",
        ],
    )

    filename = "/tmp/Worker.xlsx"
    write_styling_excel(filename, df, "worker")
    return filename
