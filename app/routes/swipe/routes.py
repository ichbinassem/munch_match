from flask import render_template, redirect, request, make_response, jsonify
from uuid import uuid4

from app.routes.swipe import bp
from app.models.swipe import Swipe
from app.models.meal import Meal
from app.models.review import Review
from app.extensions import db
from app.jwt import token_required


@bp.route("/")
@token_required
def index(user):
    """
    Route for the swiping page that allows to swipe dishes to the right/left

    Parameters:
    -------------
    user:
        User Object

    Returns:
    -----------
    swipe.html:
        A rendered template of the swipe.html file.
    """
    return render_template("./swipe/swipe.html")


@bp.route("meals")
@token_required
def getMeals(user):
    """
    Route for retrieving meals for the user to swipe
    Parameters:
    ------------
    user:
        User Object 

    Returns:
    ------------
        A response containing a message of successful retrieval of meals and a list of meals.
    """
    query = (
        Meal.query.filter(
            Meal.id.notin_(db.session.query(Swipe.meal_id).filter_by(user_id=user.id))
        )
        .limit(3)
        .all()
    )

    meals = [meal.as_dict() for meal in query]

    for meal in meals:
        reviews = Review.query.filter(Review.meal_id == meal["id"]).all()
        meal["rate"] = int(sum([review.as_dict()["rating"] for review in reviews]))

    return make_response(
        {"message": "Meals retrieved successfully", "data": meals}, 200
    )


@bp.route("/swipe/<string:uuid>/<string:direction>", methods=["POST"])
@token_required
def swipe(user, uuid, direction):
    """
    A route for showing and handling swipe requests for meals

    GET method will display three random meals that are not in the swipe table yet
    POST method will handle swipes and add them to the swipe table

    Parameters:
    ---------------
    uuid (str): 
        The UUID of the meal being swiped.
    direction (str): 
        The direction in which the meal was swiped.

    Returns:
        A response containing a message of successful swipe and a list of three random meals that have not been swiped by the user.
    """
    # Get the user ID from the session
    # user_id = db.session.get("user_id")
    meal = Meal.query.filter_by(uuid=uuid).first()

    # Add a new swipe to the database
    swipe = Swipe(
        uuid=str(uuid4()), direction=direction, user_id=user.id, meal_id=meal.id
    )
    db.session.add(swipe)
    db.session.commit()

    # Redirect to the previous page
    # Get three random meals that are not in the swipe table yet
    query = (
        Meal.query.filter(
            Meal.id.notin_(db.session.query(Swipe.meal_id).filter_by(user_id=user.id))
        )
        .limit(3)
        .all()
    )

    meals = [meal.as_dict() for meal in query]

    return make_response({"message": "Meal swipped successfully", "data": meals}, 200)
