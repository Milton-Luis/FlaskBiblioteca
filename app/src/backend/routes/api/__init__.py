from flask import Blueprint

api = Blueprint("api", __name__,url_prefix="/api")

from . import books_api, errors_api, reader_api
