from app.extensions import db


class User(db.Model):
    """
    A class representing a user in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the user.
        uuid (str): A Universally Unique Identifier (UUID) for the user.
        name (str): The user's name.
        gender (int): The user's gender (male = 0 / female = 1 / other = 2).
        email (str): The user's email.
        password (str): The user's password.
        verified (bool): A flag indicating whether the user verified the email.
        swipes (Swipe): List of swipes associated with that user.

    Methods:
        __repr__(): Returns a string representation of the User object.
    """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.Text)
    swipes = db.relationship("Swipe", backref="post")

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object, including the user name.
        """
        return f'<User "{self.name}">'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
