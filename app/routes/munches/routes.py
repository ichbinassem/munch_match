from flask import render_template, make_response
from app.models.meal import Meal
from app.models.swipe import Swipe
from app.models.review import Review
from sqlalchemy import func
from app.jwt import token_required
from app.routes.munches import bp
from app.extensions import db


@bp.route("/")
@token_required
def get_munches(user):
    """
    Get information about munches, including the cheapest, most relevant, and closest ones.

    Returns:
    --------
    A rendered HTML template that displays information about the munches:
    - munches: a list of all munches that have been swiped right by users
    - cheapest_munch: the cheapest munch that has been swiped right by users
    - relevant_munch: the most relevant munch that has been swiped right by users, based on the average rating from reviews
    - closest_munch:
    """
    query = Meal.query.filter(
        Meal.id.in_(
            db.session.query(Swipe.meal_id).filter_by(
                user_id=user.id, direction="right"
            )
        )
    ).all()

    matches = [meal.as_dict() for meal in query]

    for meal in matches:
        reviews = Review.query.filter(Review.meal_id == meal["id"]).all()
        meal["rate"] = int(sum([review.as_dict()["rating"] for review in reviews]))

    # closest_munch = to be added via google map reference
    return render_template("my_munches/swiped_dishes.html", matches=matches)


@bp.route("/<int:id>/", methods=["DELETE"])
@token_required
def delete_munches(user, id):
    """
    Get information about munches, including the cheapest, most relevant, and closest ones.

    Returns:
    --------
    A rendered HTML template that displays information about the munches:
    - munches: a list of all munches that have been swiped right by users
    - cheapest_munch: the cheapest munch that has been swiped right by users
    - relevant_munch: the most relevant munch that has been swiped right by users, based on the average rating from reviews
    - closest_munch:
    """
    Swipe.query.filter(Swipe.user_id == user.id, Swipe.meal_id == id).delete()
    db.session.commit()

    return make_response({"message": "Match removed successfully"}, 204)


@bp.route("/munch/<int:id>/")
@token_required
def get_munch(id):
    """
    Get a munch with a given id
    Parameters
    -----------
    - id: post id
    Returns
    -----------
    Munch with given id
    """
    munch = (
        Meal.query.join(Swipe)
        .filter(Swipe.direction == "right")
        .filter(Meal.id == id)
        .first()
    )

    return munch
