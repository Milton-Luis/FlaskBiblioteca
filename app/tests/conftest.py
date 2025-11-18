import os

import pytest

from app import create_app
from src.backend.extensions import configuration
from src.backend.extensions.database import db

os.environ["ENV_FOR_DYNACONF"] = "testing"


@pytest.fixture(scope="session")
def app():
    """ "Instance of Main flask app"""

    app = create_app()
    configuration.init_app(app)
    return app


@pytest.fixture
def init_database(app):
    """Fixture to initialize the database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
