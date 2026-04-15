from importlib import import_module
from dynaconf import FlaskDynaconf, Validator

def load_extensions(app):
    extensions = app.config.get("EXTENSIONS", [])

    if not extensions:
        app.logger.warning("No extensions found in the configuration.")
        return

    for extension in extensions:
        if ":" not in extension:
            raise ValueError(
                f"Invalid format for extension: {extension}. Expected 'module:function'."
            )

        module_name, factory_name = extension.split(":")

        try:
            module = import_module(module_name)
            factory = getattr(module, factory_name)
            factory(app)
            app.logger.info(f"Loaded extension: {extension}")

        except Exception as e:
            app.logger.critical(
                f"Failed to load extension: {extension}. Error: {e}"
            )
            raise 


def init_app(app, **config):
    FlaskDynaconf(app, **config)

    app.config.validators.register(
        Validator("EXTENSIONS", is_type_of=list, default=[]),
        Validator("SECRET_KEY", must_exist=True),
        # Validator("DATABASE_URL", must_exist=True),
        # Validator("FLASK_DEBUG",is_type_of=bool),
        # Validator(
        #     "DEBUG",
        #     eq=False,
        #     env="production",
        #     messages={"eq": "DEBUG deve ser False em produção"}
        # ))
    )
    
    app.config.validators.validate()