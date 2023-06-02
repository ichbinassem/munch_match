from flask import Blueprint

bp = Blueprint("review", __name__)

from app.routes.review import routes
