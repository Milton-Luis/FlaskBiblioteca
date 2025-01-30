from app.backend.extensions.database import db
from app.backend.model.models import (Admin, Books, Librarian, LendingBooks, Role,
                                      Students, User)


def create_db():
    """Create the database"""
    db.create_all()
    print("Created!")


def drop_db():
    """Drop the database."""
    db.drop_all()
    print("Cleaned!")


def init_app(app):
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))

    @app.shell_context_processor
    def make_shell_processor():
        return {
            "db": db,
            "user": User,
            "role": Role,
            "students": Students,
            "admin": Admin,
            "librarian": Librarian,
            "book": Books,
            "LendingBooks": LendingBooks
        }
