from conf import db


class UserGroup(db.Model):
    __tablename__ = "user_group"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.SmallInteger, db.ForeignKey("users.id"))
    group_id = db.Column(db.SmallInteger, db.ForeignKey("group.id"))

    @property
    def user(self):
        """The user property."""
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def group(self):
        """The group property."""
        return self._group

    @group.setter
    def group(self, value):
        self._group = value
