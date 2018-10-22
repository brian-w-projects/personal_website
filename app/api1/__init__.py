from flask import Blueprint

api1 = Blueprint('api1', __name__)

from . import views

