from conf import db
from datetime import datetime


class Worker(db.Model):
    __tablename__ = "worker"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    oid = db.Column(db.String(length=20), db.ForeignKey("struct.oid"))
    image_id = db.Column(db.SmallInteger, db.ForeignKey("image.id"), nullable=True)
    id_svup = db.Column(db.ARRAY(db.SmallInteger))
    name = db.Column(db.String(length=50))
    first_name = db.Column(db.String(length=50))
    mid_name = db.Column(db.String(length=50))
    birthday = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(length=50), nullable=True)
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
