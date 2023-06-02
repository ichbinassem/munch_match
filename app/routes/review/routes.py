from flask import render_template, request, make_response
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.routes.review import bp
from app.models.meal import Meal
from app.models.review import Review
from werkzeug.exceptions import abort
from app.jwt import token_required


@bp.route("/", methods=["POST"])
@token_required
def add_review(user):
    """
    Route that adds a review

    Parameters:
    -----------
    user: User object

    Returns:
    -----------
    dict:
        A dictionary containing the added review data
        
    Raises:
    -------
    Exception:
        If an error occurs while adding the review, returns a 500 HTTP status code
    """
    try:
        newReview = request.get_json()
        print(newReview)

        existingReview = Review.query.filter_by(
            user_id=user.id, meal_id=newReview["meal_id"]
        ).first()
        result = {}

        if not existingReview:
            newReview["uuid"] = str(uuid4())
            newReview["user_id"] = user.id
            review = Review(**newReview)

            db.session.add(review)
            db.session.commit()
            result = review.as_dict()
        else:
            existingReview.date = datetime.now()
            existingReview.rating = newReview["rating"]
            db.session.commit()
            result = existingReview.as_dict()

        return make_response(
            {"message": "Review added successfully", "newMeal": result}, 200
        )

    except Exception as error:
        error_logger.error(f"Error on adding review")
        return make_response({"message": error}, 500)
