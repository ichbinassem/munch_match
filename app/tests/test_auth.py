from app import create_app
from app.extensions import db
from app.models.user import User
import json
import unittest
from app.tests.test_config import TestConfig


class TestAuth(unittest.TestCase):
    """Test suite for the Tinder for Food authentication routes"""

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
            follow_redirects=True,
            data=json.dumps({"name": name, "email": email, "password": password}),
            headers={"Content-Type": "application/json"},
        )

    def login(self, email, password):
        """
        Test helper function that sends a POST request to the '/auth/login' route.
        Args:
            email (str): The email address of the user to log in
            password (str): The password of the user to log in
        Returns:
            The response object of the POST request
        """
        return self.app.post(
            "/auth/login",
            follow_redirects=True,
            data=json.dumps({"email": email, "password": password}),
            headers={"Content-Type": "application/json"},
        )

    def test_register(self):
        """Test registering a new user"""
        # Check if registering works
        self.register("Luis", "luis@email.com", "123456")

        # Getting user
        with self.flaskApp.app_context():
            newUser = User.query.one()

        self.assertIsNotNone(newUser)

    def test_register_email_registered(self):
        """Test registering a user with an email that is already registered"""
        # Check if registering works
        registerResponse = self.register("Luis", "luis@email.com", "123456")

        # Getting user
        with self.flaskApp.app_context():
            newUser = User.query.one()

        # Check if registering doesn't work in case email is already registered
        registerResponse = self.register("Luis", "luis@email.com", "123456")
        self.assertEqual(registerResponse.status_code, 202)

    def test_login(self):
        """Test logging in with a registered user"""
        self.register("Luis", "luis@email.com", "123456")

        # Check if login works
        loginResponse = self.login("luis@email.com", "123456")
        self.assertEqual(loginResponse.status_code, 200)

    def test_login_wrong_password(self):
        """Test logging in with a wrong password"""
        self.register("Luis", "luis@email.com", "123456")

        # Check if login doesn't work with wrong password
        loginResponse = self.login("luis@email.com", "12345")
        self.assertEqual(loginResponse.status_code, 401)

    def test_login_nonexistent_account(self):
        """Test logging in with a nonexistent account"""
        self.register("Luis", "luis@email.com", "123456")

        # Check if login doesn't work with nonexistent account
        loginResponse = self.login("test_unexistent@test.com", "123456")
        self.assertEqual(loginResponse.status_code, 404)
