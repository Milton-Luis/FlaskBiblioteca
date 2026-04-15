from flask import Flask

from src.backend.extensions import configuration
from importlib import import_module


def register_app_on_blueprint(app):
    blueprints = app.config["BLUEPRINTS"]

    for bp_path in blueprints:
        module_path, bp_name = bp_path.split(":")
        module = import_module(module_path)
        blueprint = getattr(module, bp_name)

        app.register_blueprint(blueprint)




def create_app():
    app = Flask(
        __name__, template_folder="frontend/templates", static_folder="frontend/static"
    )

    configuration.init_app(app)
    configuration.load_extensions(app)

    import src.backend.models

    register_app_on_blueprint(app)



    return app
