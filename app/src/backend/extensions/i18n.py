from flask_babel import Babel
from flask import g, request

babel = Babel()
def get_locale():
    user = getattr(g, "user", None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(["pt","en"])

def init_app(app):
    babel.init_app(app, locale_selector=get_locale)