from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, session_options={"expire_on_commit": False})

migrate = Migrate()


def init_app(app):
    return db.init_app(app), migrate.init_app(app, db, render_as_batch=True)
