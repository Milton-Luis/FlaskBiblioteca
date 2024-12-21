from flask import Flask

from app.backend.extensions import configuration


def register_blueprint_on_app(app):
    from app.backend.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.backend.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")


def create_app():
    app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")

    configuration.init_app(app)
    configuration.loader_extension(app)
    register_blueprint_on_app(app)

    return app  
