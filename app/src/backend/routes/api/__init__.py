from flask import Blueprint

api = Blueprint("api", __name__,url_prefix="/api")

from . import errors_api, users_api, books_api
