from app.extensions import db
from app.models.meal_type import meal_type


class Meal(db.Model):
    """
    A class representing a meal in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the meal.
        uuid (str): A Universally Unique Identifier (UUID) for the meal.
        name (str): The name of the meal.
        price (num): The price of the meal.
        picture (str): The picture of the meal.
        user_id (int): The ID of the user who added the meal.
        types (Type): List of types associated with that meal.
        reviews (Review): List of reviews associated with that meal.

    Methods:
        __repr__(): Returns a string representation of the Meal object.
    """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    picture = db.Column(db.Text)
    location = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    types = db.relationship("Type", secondary=meal_type, backref="posts")
    reviews = db.relationship("Review", backref="post")

    def __repr__(self):
        """
        Returns a string representation of the Meal object.

        Returns:
            str: A string representation of the Meal object, including the Meal name.
        """
        return f'<Meal "{self.name}">'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
