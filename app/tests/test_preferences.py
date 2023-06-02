from app import create_app, db
from app.models.user import User
from app.models.type import Type
from app.models.meal import Meal
from app.models.preferences import Preferences
from app.models.swipe import Swipe
import unittest
from uuid import uuid4
from app.tests.test_config import TestConfig


class TestPreferences(unittest.TestCase):
    """Test suite for the Tinder for Food preferences routes"""

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

    def test_create_preference(self):
        """
        Test creating a new preference object
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

            # Create a new preferences object
            preferecesUUID = str(uuid4())
            preference = Preferences(
                uuid=preferecesUUID,
                location="Paris",
                range=23.55,
                user_id=user.id,
                cuisine=[type],
            )
            db.session.add(preference)
            db.session.commit()

            # Verify that the preferences object was created correctly
            result = Preferences.query.filter_by(user_id=user.id).first()
            self.assertEqual(result.uuid, preferecesUUID)
            self.assertEqual(result.user_id, user.id)

    def test_update_preferences(self):
        """
        Test updating an existing preference object
        """
        with self.flaskApp.app_context():
            # Create a new preferences object
            self.test_create_preference()

            # Retrieve the old preferences object and update it
            oldPreferences = Preferences.query.filter_by(user_id=1).first()
            oldPreferences.range = 1
            oldPreferences.location = "San Francisco"
            db.session.commit()

            # Retrieve the updated preferences object and verify that it was updated correctly
            newPreferences = Preferences.query.filter_by(user_id=1).first()
            self.assertEqual(newPreferences.range, 1)
            self.assertEqual(newPreferences.location, "San Francisco")
