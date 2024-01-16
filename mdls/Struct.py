from conf import db


class Struct(db.Model):
    __tablename__ = "struct"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    oid = db.Column(db.String(length=20), primary_key=True)
    image_id = db.Column(db.SmallInteger, db.ForeignKey("image.id"), nullable=True)
    type = db.Column(db.String(length=50))
    name = db.Column(db.String)
    short_name = db.Column(db.String(length=50))
    level = db.Column(db.SmallInteger)
    active = db.Column(db.Boolean, default=True)

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
