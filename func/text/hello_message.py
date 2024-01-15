import time

from mdls import User


def hello_message(user: User) -> str:
    """
    Формируем приветсвенное сообщение, для пользователя
    """

    temp = int(time.strftime("%H"))

    hello = {
        0 <= temp < 6: "Доброй ночи, ",
        6 <= temp < 11: "Доброе утро, ",
        11 <= temp < 16: "Добрый день, ",
        16 <= temp < 22: "Добрый вечер, ",
        22 <= temp < 24: "Доброй ночи, ",
    }[True] + user.fio

    text = f"""
    *{hello}*\n
    Этот бот должен облегчить Вам работу по ведению табеля штатного расписания
    Доступные Вам группы работников:
    """

    return text
