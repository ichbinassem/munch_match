from app.extensions import db
from app.models.type import Type
from app.models.preferences_type import preferences_type


class Preferences(db.Model):
    """
    A class representing a meal in the tinder for food app.

    Attributes:

    Methods:
        __repr__(): Returns a string representation of the Meal object.
    """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    location = db.Column(db.String(150), default="")
    range = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    cuisine = db.relationship("Type", secondary=preferences_type, backref="cuisines")

    def __repr__(self):
        """
        Returns a string representation of the Meal object.

        Returns:
            str: A string representation of the Meal object, including the Meal name.
        """
        return f'<Preferences for user with id "{self.user_id}">'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
