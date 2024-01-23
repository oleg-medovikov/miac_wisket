from conf import db


class Journal(db.Model):
    """
    таблица ведения журнала посещаемости сотрудников
    """

    __tablename__ = "journal"
    __table_args__ = {"extend_existing": True}

    day = db.Column(db.Date, comment="Дата")
    worker_id = db.Column(
        db.SmallInteger, db.ForeignKey("worker.id"), comment="Идентификатор сотрудника"
    )
    time_start = db.Column(db.Time, nullable=True, comment="Приход на работу")
    time_stop = db.Column(db.Time, nullable=True, comment="Уход с работы")
    time_lose = db.Column(
        db.SmallInteger, nullable=True, comment="Потерянное время (минуты)"
    )
    time_win = db.Column(db.SmallInteger, nullable=True, comment="Переработка (минуты)")

    time_remote_start = db.Column(
        db.Time, nullable=True, comment="Время подключения на удаленку"
    )
    time_remote_stop = db.Column(
        db.Time, nullable=True, comment="Время отключения от удаленки"
    )

    time_remote = db.Column(
        db.SmallInteger, nullable=True, comment="Общее время подключения (минуты)"
    )
    # добавлю на всякий случай
    status = db.Column(
        db.SmallInteger, db.ForeignKey("status.id"), nullable=True, comment="оправдание"
    )
