from conf import db


class Struct(db.Model):
    __tablename__ = "struct"
    __table_args__ = {"extend_existing": True}

    oid = db.Column(db.String(length=20), primary_key=True, comment="код подразделения")
    image_id = db.Column(
        db.SmallInteger, db.ForeignKey("image.id"), nullable=True, comment="id картинки"
    )
    kind = db.Column(db.String(length=50), comment="Тип подраздеения")
    name = db.Column(db.String, comment="Название")
    short_name = db.Column(
        db.String(length=50), comment="Краткое название (50 символов)"
    )
    level = db.Column(db.SmallInteger, comment="Уровень")
    active = db.Column(db.Boolean, default=True, comment="активно")

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
