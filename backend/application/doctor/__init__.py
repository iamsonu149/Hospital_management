from flask import Blueprint

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

from . import routes
