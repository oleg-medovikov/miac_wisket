from conf import db
from datetime import datetime


class Group(db.Model):
    __tablename__ = "group"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    image_id = db.Column(db.SmallInteger, db.ForeignKey("image.id"), nullable=True)
    name = db.Column(db.String)
    short_name = db.Column(db.String(length=50))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
