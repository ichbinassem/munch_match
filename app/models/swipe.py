from app.extensions import db


class Swipe(db.Model):
    """
    A class representing a swipe in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the swipe.
        uuid (str): A Universally Unique Identifier (UUID) for the swipe.
        direction (int): The direction of the swipe (left = 0 / right = 1).
        user_id (int): The ID of the user who swiped.
        meal_id (int): The ID of the meal that was swiped.
        all_swipes(list): All of the swipes a user currently has

    Methods:
        __repr__(): Returns a string representation of the Swipe object.
    """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    direction = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))

    def __repr__(self):
        """
        Returns a string representation of the Swipe object.

        Returns:
            str: A string representation of the Swipe object, including the swipe uuid.
        """
        return f'<Swipe "{self.uuid}">'
