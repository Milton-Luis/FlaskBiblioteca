import pytest
from dynaconf import settings

from src import create_app


@pytest.fixture
def app():
    app = create_app()

    yield app
