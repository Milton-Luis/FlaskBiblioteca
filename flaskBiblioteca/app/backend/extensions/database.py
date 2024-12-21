from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# from sqlalchemy.orm import registry

# def mapper_config():
#     """mapper_config

#     this function is similiar to the Base superclass with declarativeBase
#     * variables -> [mapper_registry]

#     * [registry()] function that creates new 'MapperRegistry, used to manage mappings between classes and database tables

#     Returns:
#         mapper_registry: returns the generate_base() function generates a new base class that contain metada and methods for all mapped classes
#     """
#     mapper_registry = registry()
#     return mapper_registry.generate_base()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, session_options={"expire_on_commit": False})

migrate = Migrate()


def init_app(app):
    return db.init_app(app), migrate.init_app(app, db, render_as_batch=True)
