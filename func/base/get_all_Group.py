from pandas import DataFrame

from mdls import Group, User, Image
from conf import db


async def get_all_group() -> str:
    """Вытаскиваем все группы и возвращаем путь до файла"""

    DATA = (
        await db.select(
            [
                Group.id,
                Group.image_id,
                Image.name,
                Group.name,
                Group.short_name,
                User.fio,
                Group.date_update,
            ]
        )
        .select_from(Group.join(User).join(Group))
        .order_by(Group.id)
        .gino.all()
    )

    df = DataFrame(data=DATA)

    filename = "/tmp/Groups.xlsx"
    df.to_excel(filename, index=False)
    return filename
