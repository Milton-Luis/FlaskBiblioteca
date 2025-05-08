import pytest
from app.backend.extensions.database import db
from app.backend.model.models import Books, User

from .test_base_app import app


@pytest.fixture
def init_database(app):
    """Fixture to initialize the database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_create_user(init_database):
    """Test case to verify user creation."""
    user = User(
        firstname="John",
        lastname="Doe",
        fullname="John Doe",
        email="johndoe@teste.com",
        phone="(35) 99563-1123",
    )
    init_database.session.add(user)
    init_database.session.commit()
    assert user.id is not None


def test_add_book(init_database):
    """Test case to verify book addition."""

    book = Books(
        title="Flask for Beginners",
        author="John Doe",
        isbn="978-3-16-148410-0",
        total_of_books=5,
        available_quantity=5,
    )
    init_database.session.add(book)
    init_database.session.commit()
    assert book.id is not None
