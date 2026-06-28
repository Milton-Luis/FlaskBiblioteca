import pytest
from dynaconf import settings
from src import create_app

settings.configure(ENV_FOR_DYNACONF="testing")

@pytest.fixture
def app():
    app = create_app()

    yield app
