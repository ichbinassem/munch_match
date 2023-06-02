import os

# Set up a test database
TEST_DB = "test.db"
basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """
    Testing Configuration settings for the Flask app.
    Attributes:
    - TESTING: Testing state
    - WTF_CSRF_ENABLED: Whether CSRF protection is enabled
    - DEBUG: Debug mode
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - LOG_FILE_NAME: Log file name
    - MEALS_CREATED: How many meals should be created
    """

    # Whether testing mode is enabled
    TESTING = True

    # Whether CSRF protection is enabled
    WTF_CSRF_ENABLED = True

    # Whether debug mode is enabled
    DEBUG = False

    # The connection URI for the test database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, TEST_DB)

    # The name of the log file for testing
    LOG_FILE_NAME = "log-test.txt"

    # Whether SQLAlchemy should track modifications to models
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # The number of test meals to create
    MEALS_CREATED = 0
