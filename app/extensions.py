from flask_sqlalchemy import SQLAlchemy
import logging

# Initializing db on SQLAlchemy
db = SQLAlchemy(session_options={
    'expire_on_commit': False
})


def setFormatter(fileName):
    """Creates a file handler with a formatter for logging

    Args:
    fileName (str): name of the log file to write

    Returns:
    logging.FileHandler: a file handler with a formatter for logging
    """
    # Setting up logging handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(fileName)
    file_handler.setFormatter(formatter)

    return file_handler


# Setting up logger
info_logger = logging.getLogger(f"munch_match_info")
info_logger.setLevel(logging.INFO)

# Setting up logger
error_logger = logging.getLogger(f"munch_match_error")
error_logger.setLevel(logging.ERROR)
