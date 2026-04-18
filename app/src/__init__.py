from importlib import import_module

from flask import Flask

from src.backend.extensions import configuration


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

    # Replace ${INSTANCE_PATH} with actual instance path
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('${INSTANCE_PATH}', app.instance_path)

    import src.backend.models

    register_app_on_blueprint(app)

    return app
