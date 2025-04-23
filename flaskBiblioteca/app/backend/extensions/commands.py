import os
from getpass import getpass

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
    os.system("clear")
    print("Bem vindo ao shell para criação de acesso admin")
    firstname = input("Informe seu nome: ").capitalize()
    lastname = input("Informe seu sobrenome: ").capitalize()
    email = input("Informe seu email: ")
    password = getpass("Informe sua senha: ")
    confirm = getpass("Confirme sua senha: ")
    role = "admin"
    admin = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        roles=Admin(
            rolename=role,
            is_admin=True,
            is_confirmed=True,
            password=generate_password(password),
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
            "students": Students,
            "admin": Admin,
            "librarian": Librarian,
            "books": Books,
            "lending_books": LendingBooks,
        }
