from flask import Flask

from src.backend.extensions import configuration


def register_app_on_blueprint(app):
    from src.backend.routes.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from src.backend.routes.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)


def create_app():
    app = Flask(
        __name__, template_folder="frontend/templates", static_folder="frontend/static"
    )

    register_app_on_blueprint(app)
    configuration.init_app(app)
    configuration.load_extensions(app)

    return app
