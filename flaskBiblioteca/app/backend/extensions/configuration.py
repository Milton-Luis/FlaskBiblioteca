from dynaconf import FlaskDynaconf


def loader_extension(app):
    """Load all the extensions"""
    return app.config.load_extensions(key="EXTENSIONS")


def init_app(app):
    return FlaskDynaconf(app)