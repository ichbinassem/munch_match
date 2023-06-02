from flask import request, jsonify, redirect
from config import Config
from app.models.user import User
import jwt
from functools import wraps


def getCookie(name):
    """
    Extracts the value of a cookie with the given name from the
    request headers.

    Args:
        name (str): The name of the cookie to extract.

    Returns:
        str: The value of the cookie.
    """
    value = f"; {request.headers['Cookie']}"
    parts = value.split(f"; {name}=")
    if len(parts) == 2:
        return parts.pop().split(";")[0]


def token_required(f):
    """
    Decorator function to require a JWT token for accessing certain routes.
    Extracts the JWT token from the request header, decodes it to fetch the
    stored details, and returns the current logged-in user's context to the route.
    In case the JWT token is not found, redirects user to login

    Args:
        f: The function to be decorated.

    Returns:
        Function: The decorated function.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            # JWT is passed in the request header
            if getCookie("user_uuid"):
                token = getCookie("user_uuid")
            else:
                return redirect("/auth")
        except:
            return redirect("/auth")

        try:
            # Decoding the payload to fetch the stored details. Returning the
            # user and tasks to the decorated function
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user = User.query.filter_by(uuid=data["uuid"]).first()
        except Exception as e:
            return redirect("/auth")

        # Returns the current logged in user and tasks to the routes
        return f(user, *args, **kwargs)

    return decorated
