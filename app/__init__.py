from flask import Flask, redirect
from app.populate import add_types, generateInitialMeals
from config import Config
from app.extensions import db, setFormatter, info_logger, error_logger
from app.models.user import User
from app.models.type import Type
from app.models.meal import Meal
from app.models.review import Review
from app.models.swipe import Swipe
from app.models.preferences import Preferences


def create_app(config_class=Config):
    """
    This function creates a Flask application instance and returns it.

    Parameters:
        config_class (Config): A configuration class to configure the Flask app
        instance. Defaults to `Config`, which comes from the configuration file
        that reads the environment variables.

    Returns:
        Flask: The Flask application instance.

    """
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config_class)

    # Initializing extensions
    fileFormatter = setFormatter(config_class.LOG_FILE_NAME)
    info_logger.addHandler(fileFormatter)
    error_logger.addHandler(fileFormatter)
    info_logger.info("File log for Tinder for Food opened")

    db.init_app(flaskApp)

    info_logger.info("DB Initiated")
    with flaskApp.app_context():
        db.create_all()
        info_logger.info("Tables created on DB")

    with flaskApp.app_context():
        add_types()
        generateInitialMeals(config_class.MEALS_CREATED)

    # Registering blueprints
    @flaskApp.errorhandler(404)
    def notFound(e):
        return redirect("/auth")

    from app.routes.auth import bp as auth_bp

    flaskApp.register_blueprint(auth_bp, url_prefix="/auth/")

    from app.routes.swipe import bp as swipe_bp

    flaskApp.register_blueprint(swipe_bp, url_prefix="/swipe/")

    from app.routes.preferences import bp as preferences_bp

    flaskApp.register_blueprint(preferences_bp, url_prefix="/preferences/")

    from app.routes.meal import bp as meal_bp

    flaskApp.register_blueprint(meal_bp, url_prefix="/meal/")

    from app.routes.account import bp as account_bp

    flaskApp.register_blueprint(account_bp, url_prefix="/account/")

    from app.routes.munches import bp as munches_bp

    flaskApp.register_blueprint(munches_bp, url_prefix="/munches/")

    from app.routes.review import bp as review_bp

    flaskApp.register_blueprint(review_bp, url_prefix="/review/")

    return flaskApp
