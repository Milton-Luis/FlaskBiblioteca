from importlib import import_module

from dynaconf import FlaskDynaconf


def load_extensions(app):
    extensions = app.config.get("EXTENSIONS", [])

    if not extensions:
        app.logger.warning("No extensions found in the configuration.")
        return

    for extension in extensions:
        try:
            if ":" not in extension:
                app.logger.error(f"Invalid format for extension: {extension}. Expected 'module:factory'.")
            else:
                module_name, factory = extension.split(":")
                ext = import_module(module_name)
                extension_class = getattr(ext, factory)
                extension_class(app)
        except Exception as e:
            app.logger.error(f"Failed to load extension: {extension}. Error: {e}")

def init_app(app, **config):
    return FlaskDynaconf(app, **config)