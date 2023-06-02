from flask import Blueprint

bp = Blueprint("swipe", __name__)

from app.routes.swipe import routes
