from app.src import create_app
from dynaconf import settings
import pytest

@pytest.fixture
def app():
    
    app = create_app()

    yield app
