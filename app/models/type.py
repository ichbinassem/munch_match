from app.extensions import db


class Type(db.Model):
    """
    A class representing a type in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the type.
        uuid (str): A Universally Unique Identifier (UUID) for the type.
        name (str): The type's name.

    Methods:
        __repr__(): Returns a string representation of the Type object.
    """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    name = db.Column(db.String(150))

    def __repr__(self):
        """
        Returns a string representation of the Type object.

        Returns:
            str: A string representation of the Type object, including the type name.
        """
        return f'<Type "{self.name}">'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
