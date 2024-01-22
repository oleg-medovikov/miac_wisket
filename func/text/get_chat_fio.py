from aiogram.types import Message

LIST = ["username", "first_name", "last_name"]


def get_chat_fio(mess: Message) -> str:
    "Берем полное имя пользователя телеграма из сообщения"
    return " ".join([str(mess.chat.__dict__.get(_, "")) for _ in LIST])
