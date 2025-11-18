import os
from getpass import getpass

from src.backend.extensions.database import db
from src.backend.extensions.security import generate_password
from src.backend.models.models import Admin, Books, LendingBooks, Librarian, Role, User


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
    os.system("clear")
    print("Bem vindo ao shell para criação de acesso admin")
    firstname = input("Informe seu nome: ").capitalize()
    lastname = input("Informe seu sobrenome: ").capitalize()
    email = input("Informe seu email: ").lower()
    phone = input("Informe seu número de telefone: ")
    password = getpass("Informe sua senha: ")
    confirm = getpass("Confirme sua senha: ")
    admin = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        is_confirmed=True,
        password=generate_password(password),
        role=Admin(
            is_admin=True,
        ),
    )
    admin.fullname = admin.set_fullname(firstname, lastname)
    try:
        if confirm != password:
            print("As senhas não conferem!")
            return
    except Exception as e:
        print(e)
        db.session.rollback()
    else:
        db.session.add(admin)
        db.session.commit()
        print("Super user created!")
    finally:
        db.session.close()


def init_app(app):
    for command in [create_db, drop_db, createSuperUser]:
        app.cli.add_command(app.cli.command()(command))

    @app.shell_context_processor
    def make_shell_processor():
        return {
            "db": db,
            "users": User,
            "roles": Role,
            "admin": Admin,
            "librarian": Librarian,
            "books": Books,
            "lending_books": LendingBooks,
        }
