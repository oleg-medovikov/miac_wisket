from conf import db
from datetime import datetime


class UserLog(db.Model):
    """
    тут храним действия пользователей и неизвестных,
    потревоживших бота
    """

    __tablename__ = "users_log"
    __table_args__ = {"extend_existing": True}

    time = db.Column(db.DateTime, primary_key=True, default=datetime.now())
    user_id = db.Column(db.SmallInteger, db.ForeignKey("users.id"), nullable=True)
    event_id = db.Column(db.SmallInteger, nullable=True)
    event = db.Column(db.String, nullable=True)

    @property
    def user(self):
        """The user property."""
        return self._user

    @user.setter
    def user(self, value):
        self._user = value
