from src.backend.extensions.flask_argon2 import Argon2

argon2 = Argon2()


def init_app(app):
    return argon2.init_app(app)
