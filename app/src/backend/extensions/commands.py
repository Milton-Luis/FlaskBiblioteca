import os
from getpass import getpass

from src.backend.extensions.database import db
from src.backend.extensions.security import generate_password
from src.backend.models.books import Books
from src.backend.models.loan import BookLoan
from src.backend.models.users import User
from src.backend.models.roles import Roles, Admin, Librarian
from src.backend.services.seeds import seed_roles


def create_db():
    """Create the database"""
    db.create_all()
    print("Created!")


def drop_db():
    """Drop the database."""
    db.drop_all()
    print("Cleaned!")


def create_super_user():
    """Cria super user, apenas se não existir"""
    os.system("clear")
    print("Bem-vindo ao shell para criação de super user")

    # Verifica se já existe super user
    existing_super = db.session.query(User).join(Roles).filter_by(type="admin").first()
    if existing_super:
        print(f"Super user já existe: {existing_super.email}")
        return

    # Recupera role Admin
    admin_role = db.session.query(Roles).filter_by(type="admin").first()
    if not admin_role:
        return

    email = input("Informe seu email: ").lower()

    while True:
        password = getpass("Informe sua senha: ")
        confirm = getpass("Confirme sua senha: ")
        if confirm != password:
            print("As senhas não conferem!")
        else:
            break

    # Cria super user
    super_user = User(
        email=email,
        is_confirmed=True,
        password=generate_password(password),
        role=admin_role,
    )

    try:
        db.session.add(super_user)
        db.session.commit()
        print(f"Super user criado: {email}")
    except Exception as e:
        print("Erro ao criar super user:", e)
        db.session.rollback()


def seed_all():
    """Seed defaultRoless"""
    seed_roles()
    print("seeded!!")


def init_app(app):
    for command in [create_db, drop_db, seed_all, create_super_user]:
        app.cli.add_command(app.cli.command()(command))

    @app.shell_context_processor
    def make_shell_processor():
        return {
            "db": db,
            "users": User,
            "roles": Roles,
            "admin": Admin,
            "librarian": Librarian,
            "books": Books,
            "loan_books": BookLoan,
        }
