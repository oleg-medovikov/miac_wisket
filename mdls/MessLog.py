from conf import db


class MessLog(db.Model):
    """
    запоминаем номер сообщения в чате пользователя
    """

    __tablename__ = "mess_log"
    __table_args__ = {"extend_existing": True}

    tg_id = db.Column(db.BigInteger, primary_key=True)
    image_id = db.Column(db.SmallInteger, db.ForeignKey("image.id"), nullable=True)
    mess_id = db.Column(db.BigInteger)

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
