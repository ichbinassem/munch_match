from dotenv import load_dotenv
from os import environ as env
import os
import pymysql
import urllib

# Set the default database driver to MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration settings for the Flask app.
    Attributes:
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - SQLALCHEMY_TRACK_MODIFICATIONS: Whether the app will track DB authentication or not
    - SECRET_KEY: Secret key for the app
    - LOG_FILE_NAME: Log file name
    - MEALS_CREATED: How many meals should be created
    """

    # Set the connection URI for the database
    # SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"\
    #     or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://tinder_for_food_user:tinder_for_food_password@db/tinder_for_food"
    )

    # Enable tracking modifications to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Set the secret key for the app
    SECRET_KEY = env["SECRET_KEY"] if hasattr(env, "SECRET_KEY") else "testing_secret"
    LOG_FILE_NAME = "log.txt"
    MEALS_CREATED = 5
