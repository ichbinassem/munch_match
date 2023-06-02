from flask import Blueprint

bp = Blueprint("meal", __name__)

from app.routes.meal import routes
