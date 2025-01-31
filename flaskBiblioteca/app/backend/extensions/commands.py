from app.backend.extensions.database import db
from app.backend.extensions.security import generate_password
from app.backend.model.models import (Admin, Books, LendingBooks, Librarian,
                                      Role, Students, User)


def create_db():
    """Create the database"""
    db.create_all()
    print("Created!")


def drop_db():
    """Drop the database."""
    db.drop_all()
    print("Cleaned!")

def createSuperUser():
    """Create a super user"""
    firstname = input("informe seu nome: ").capitalize()
    lastname = input("informe seu sobrenome: ").capitalize()
    email = input("Informe seu email: ")
    password = input("Informe sua senha: ")
    role="admin"
    admin = User(firstname=firstname, lastname=lastname, email=email, roles=Admin(rolename=role, is_admin=True, is_confirmed=True,  password=generate_password(password)))

    db.session.add(admin)
    db.session.commit()
    print("Super user created!")

def init_app(app):
    for command in [create_db, drop_db, createSuperUser]:
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
            "lending_books": LendingBooks
        }
