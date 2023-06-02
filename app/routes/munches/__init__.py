from flask import Blueprint

bp = Blueprint("munches", __name__)

from app.routes.munches import routes
