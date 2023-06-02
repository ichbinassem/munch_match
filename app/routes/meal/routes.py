from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.routes.meal import bp
from app.models.meal import Meal
from app.models.review import Review
from werkzeug.exceptions import abort
from app.jwt import token_required


@bp.route("/", methods=["POST"])
@token_required
def add_meal(user):
    """
    Route that allows a user to create a new meal

    Parameters:
    -----------
    user: User
        User object that is authenticated using the JWT token.

    Returns:
    --------
    response: dict
        A dictionary containing the message and the newly created meal if the operation was successful.
 
    Raises:
    -------
    Exception:
        If there is an error adding the meal to the database.

    """
    try:
        newData = request.get_json()
        newData["uuid"] = str(uuid4())
        newData["user_id"] = user.id

        newMeal = Meal(**newData)
        db.session.add(newMeal)
        db.session.commit()
        newMeal = newMeal.as_dict()

        reviews = Review.query.filter(Review.meal_id == newMeal["id"]).all()
        newMeal["rate"] = int(sum([review.as_dict()["rating"] for review in reviews]))

        return make_response(
            {"message": "Meal created successfully!", "newMeal": newMeal}, 201
        )
    except Exception as error:
        error_logger.error(f"Error on adding meal")
        return make_response({"message": error}, 500)
