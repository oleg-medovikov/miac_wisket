from conf import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    oid = db.Column(db.String(length=20), db.ForeignKey("struct.oid"), nullable=True)
    tg_id = db.Column(db.BigInteger)
    fio = db.Column(db.String(length=200))
    admin = db.Column(db.Boolean)
    date_update = db.Column(db.DateTime(), default=datetime.now())
