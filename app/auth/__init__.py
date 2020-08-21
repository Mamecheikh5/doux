from flask import Blueprint

auth_microservice = Blueprint('auth_microservice', __name__)

from . import views