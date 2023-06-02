from app import create_app, db
from app.models.user import User
from app.models.type import Type
from app.models.meal import Meal
from app.models.swipe import Swipe
from app.models.review import Review
import unittest
from uuid import uuid4
from datetime import datetime
from app.tests.test_config import TestConfig


class TestMeal(unittest.TestCase):
    """Test suite for the Tinder for Food meal routes"""

    def setUp(self):
        """Set up Tinder for Food app, database, and test client"""
        self.flaskApp = create_app(TestConfig)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(self.flaskApp.debug, False)

    def tearDown(self):
        """Clean up after the test"""
        pass

    def test_create_meal(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            # Create a new user
            userUUID = str(uuid4())
            user = User(
                uuid=userUUID,
                name="Alice",
                email="alice@gmail.com",
                password="1234cat",
            )
            db.session.add(user)
            db.session.commit()

            # Create a new cuisine type
            typeUUID = str(uuid4())
            type = Type(uuid=typeUUID, name="Italian")
            db.session.add(type)
            db.session.commit()

            # Create a new meal object
            mealUUID = str(uuid4())
            meal = Meal(
                uuid=mealUUID,
                name="Test Meal",
                price=23.55,
                picture="test_pic",
                location="Paris",
                user_id=user.id,
                types=[type],
            )
            db.session.add(meal)
            db.session.commit()

            # Verify that the meal object was created correctly
            result = Meal.query.filter_by(user_id=user.id).first()
            self.assertEqual(result.uuid, mealUUID)
            self.assertEqual(result.user_id, user.id)

    def test_swipe_right_meal(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            self.test_create_meal()
            newMeal = Meal.query.filter_by(id=1).first()
            newUser = User.query.filter_by(id=1).first()

            newSwipe = Swipe(
                **{
                    "uuid": str(uuid4()),
                    "meal_id": newMeal.id,
                    "user_id": newUser.id,
                    "direction": "right",
                }
            )
            db.session.add(newSwipe)
            db.session.commit()

            self.assertEqual(newSwipe.id, 1)

    def test_swipe_left_meal(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            self.test_create_meal()
            newMeal = Meal.query.filter_by(id=1).first()
            newUser = User.query.filter_by(id=1).first()

            newSwipe = Swipe(
                **{
                    "uuid": str(uuid4()),
                    "meal_id": newMeal.id,
                    "user_id": newUser.id,
                    "direction": "left",
                }
            )
            db.session.add(newSwipe)
            db.session.commit()

            self.assertEqual(newSwipe.id, 1)

    def test_swipe_remove(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            self.test_swipe_left_meal()
            newMeal = Meal.query.filter_by(id=1).first()
            newUser = User.query.filter_by(id=1).first()

            existingSwipe = Swipe.query.filter_by(
                meal_id=newMeal.id, user_id=newUser.id
            ).delete()
            db.session.commit()
            existingSwipe = Swipe.query.filter_by(
                meal_id=newMeal.id, user_id=newUser.id
            ).first()

            self.assertIsNone(existingSwipe)

    def test_add_review(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            newReview = {
                "rating": 5,
            }

            self.test_swipe_left_meal()
            newUser = User.query.filter_by(id=1).first()
            newMeal = Meal.query.filter_by(id=1).first()
            existingReview = Review.query.filter_by(
                user_id=newUser.id, meal_id=newMeal.id
            ).first()

            if not existingReview:
                newReview["uuid"] = str(uuid4())
                newReview["user_id"] = newUser.id
                newReview["meal_id"] = newMeal.id
                review = Review(**newReview)

                db.session.add(review)
                db.session.commit()
                result = review.as_dict()
            else:
                existingReview.date = datetime.now()
                existingReview.rating = newReview["rating"]
                db.session.commit()
                result = existingReview.as_dict()

            self.assertIsNotNone(result)

    def test_get_meal_review(self):
        """
        Test creating a new meal object
        """
        with self.flaskApp.app_context():
            self.test_add_review()
            newUser = User.query.filter_by(id=1).first()
            newMeal = Meal.query.filter_by(id=1).first()
            reviews = Review.query.filter(Review.meal_id == newMeal.id).all()

            newMeal = newMeal.as_dict()
            newMeal["rate"] = int(
                sum([review.as_dict()["rating"] for review in reviews])
            )

            self.assertIsNotNone(newMeal["rate"], 5)
