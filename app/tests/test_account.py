from app import create_app
from app.extensions import db
from app.models.user import User
from app.tests.test_config import TestConfig
import unittest
import json

# Sample user data to use in tests
user = {"name": "Jessica", "email": "jessica@gmail.com", "password": "password"}


class TestAccount(unittest.TestCase):
    """Test suite for the account routes"""

    def setUp(self):
        """Set up app, database, and test client"""
        self.flaskApp = create_app(TestConfig)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()
        self.assertEqual(self.flaskApp.debug, False)

    def tearDown(self):
        """Clean up after the test"""
        pass

    def register(self, name, email, password):
        """
        Test helper function that sends a POST request to the '/auth/register' route.
        Args:
            name (str): The name of the user to register
            email (str): The email address of the user to register
            password (str): The password of the user to register
        Returns:
            The response object of the POST request
        """
        return self.app.post(
            "/auth/register",
            data=json.dumps({"name": name, "email": email, "password": password}),
            follow_redirects=True,
            headers={"Content-Type": "application/json"},
        )

    def test_email_update(self):
        """Test updating a user's email address"""
        with self.flaskApp.app_context():
            # Register a new user
            self.register(**user)

            # Get the user from the database
            newUser = db.session.query(User).filter(User.id == 1).first()

            # Update the user's email address
            newUser.email = "newemail@gmail.com"
            db.session.commit()

        # Verify that the user's email address was updated correctly
        self.assertNotEqual(newUser.email, "jessica@gmail.com")
        self.assertEqual(newUser.email, "newemail@gmail.com")

    def test_name_update(self):
        """Test updating a user's name"""
        with self.flaskApp.app_context():
            # Register a new user
            self.register(**user)

            # Get the user from the database
            newUser = db.session.query(User).filter(User.id == 1).first()

            # Update the user's name
            newUser.name = "Jess"
            db.session.commit()

        # Verify that the user's name was updated correctly
        self.assertNotEqual(newUser.name, "Jessica")
        self.assertEqual(newUser.name, "Jess")
