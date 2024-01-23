from conf import db


class Status(db.Model):
    """
    таблица статусов сотрудников, для ведения журнала
    """

    __tablename__ = "status"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    text = db.Column(db.String)
