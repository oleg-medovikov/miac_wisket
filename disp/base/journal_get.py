from disp.base import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot
import logging
from sqlalchemy import func, and_
import pandas as pd
import locale


from func import update_message, add_keyboard, highlight_time, write_file
from mdls import User, Worker, Struct, Journal
from conf import CallAny, db

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


@router.callback_query(CallAny.filter(F.action == "journal_get"))
async def journal_get(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут вытаскиваются непосредственно журнал
    -- определить юзера
    -- нужно определить всех воркеров пользователя
    --
    """

    logging.info(f"!!! {callback_data}")

    if callback_data.user_id:
        user = await User.get(callback_data.user_id)
    else:
        user = await User.query.where(User.tg_id == callback.from_user.id).gino.first()

    # select * from worker where oid like '1.2.%.%' order by oid, chief desc;

    # Используем метод query для создания запроса
    patern = user.oid.replace("0", "%")
    workers = await (
        Worker.load(struct=Struct)
        .query.where(Worker.oid.like(patern))
        .order_by(Worker.oid, Worker.chief.desc())
        .gino.all()
    )
    # Выполняем запрос и получаем результаты
    worker_ids = [_.id for _ in workers]

    query = (
        db.select(
            [
                Struct.kind,
                Struct.name,
                Worker.oid,
                Worker.chief,
                (
                    Worker.name
                    + " "
                    + func.substr(Worker.first_name, 1, 1)
                    + ". "
                    + func.substr(Worker.mid_name, 1, 1)
                    + "."
                ).label("fio"),
                Journal.day,
                Journal.time_start,
                Journal.time_stop,
            ]
        )
        .select_from(Journal.join(Worker).join(Struct))
        .where(
            and_(
                func.extract("year", Journal.day) == callback_data.year,
                func.extract("month", Journal.day) == callback_data.month,
                Journal.worker_id.in_(worker_ids),
            )
        )
    )

    # Выполняем запрос и получаем результаты
    journal_entries = await query.gino.all()
    if len(journal_entries) == 0:
        # выход сообщения что нет доступных записей журнала, что странно
        return
    columns = [
        "kind",
        "struct",
        "oid",
        "chief",
        "fio",
        "day",
        "time_start",
        "time_stop",
    ]
    df = pd.DataFrame(data=journal_entries, columns=columns)
    df["week"] = pd.to_datetime(df.day).dt.strftime("%A")
    df_sorted = df.sort_values("day")

    p = df_sorted.pivot(
        index=["oid", "struct", "kind", "fio"],
        columns=["day", "week"],
        values=["time_start", "time_stop"],
    ).stack(0, future_stack=True)
    p = p.fillna("")
    p = p.style.map(highlight_time)

    file = "/tmp/table.xlsx"
    # p.to_excel(file)
    write_file(p, file)

    dict_ = {"назад": CallAny(action="start").pack()}
    mess = "Заполните файл и киньте мне его обратно в чат. Я применю изменения"
    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            mess,
            add_keyboard(dict_),
            image_name="files",
            file_path=file,
        )
