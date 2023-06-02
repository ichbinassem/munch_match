import jwt

from flask import render_template, request, make_response, redirect, url_for, jsonify
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
from config import Config

from app.routes.auth import bp
from app.models.user import User
from app.models.preferences import Preferences
from app.extensions import db, info_logger, error_logger
from config import Config


@bp.route("/")
def auth():
    return render_template("./auth/auth.html")


@bp.route("/login/", methods=["POST"])
def login():
    """
    A route for logging in a user.

    GET requests will display the login page, while POST requests
    will attempt to log in the user.

    Returns:
        A rendered template containing the login page (for GET requests),
        or a response object indicating success or failure (for POST requests).
    """
    try:
        userData = request.get_json()

        existingUser = User.query.filter_by(email=userData["email"]).first()

        info_logger.info(f"Client tried to log in with email: {userData['email']}")

        if not existingUser:
            error_logger.error(f"User not found with email: {userData['email']}")
            return make_response({"message": "User not found"}, 404)
        # Compares the password with the hashed password stored in the database
        elif check_password_hash(existingUser.password, userData["password"]):
            jwtToken = jwt.encode(
                {
                    "uuid": existingUser.uuid,
                    "exp": datetime.utcnow() + timedelta(days=1),
                },
                Config.SECRET_KEY,
            )

            info_logger.info(
                f"User successfully log in with email: {userData['email']}"
            )

            response = make_response({"message": "User logged in!"}, 200)
            response.set_cookie("user_uuid", jwtToken)

            return response
        error_logger.error(
            f"User tried to log in with email: {userData['email']}, but used the wrong password"
        )
        return make_response({"message": "Wrong password"}, 401)
    except Exception as error:
        error_logger.error(f"Error on log in")
        return make_response({"message": error}, 500)


@bp.route("/register/", methods=["POST"])
def register():
    """
    A route for registering a new user.

    GET requests will display the registration page, while POST
    requests will attempt to create a new user.

    Returns:
        A rendered template containing the registration page (for GET
        requests), or a response object indicating success or failure
        (for POST requests).
    """
    try:
        newUserData = request.get_json()
        newUserData["uuid"] = str(uuid4())
        info_logger.info(f"Client tried to log in with email: {newUserData['email']}")

        existingUser = User.query.filter_by(email=newUserData["email"]).first()

        if not existingUser:
            # Hashes the password for saving in the database
            newUserData["password"] = generate_password_hash(newUserData["password"])
            user = User(**newUserData)
            db.session.add(user)
            db.session.commit()

            newPreferences = Preferences(
                **{"uuid": str(uuid4()), "range": 2.5, "user_id": user.id}
            )
            db.session.add(newPreferences)
            db.session.commit()

            info_logger.info(f"User registered with email: {newUserData['email']}")

            return make_response(
                {
                    "message": "User created successfully!\
                                    Enter your email to verify your account.\
                                    Remember to check your spam folder. (You may need\
                                    to mark as not a Span to access the link)"
                },
                201,
            )
        else:
            info_logger.info(
                f"User already registered with email: {newUserData['email']}"
            )
            return make_response(
                {"message": "This email is already registered! Login now"}, 202
            )
    except Exception as error:
        error_logger.error(f"Error on registering")
        return make_response({"message": error}, 500)


@bp.route("/logout/")
def logout():
    """
    A route for logging out a user.

    Returns:
        A response object indicating success.
    """
    info_logger.info(f"User logged out")
    response = make_response({"message": "User logged out!"}, 200)
    response.set_cookie("user_uuid", expires=0)

    return response


@bp.errorhandler(404)
def notFound():
    return redirect("/auth/login")
