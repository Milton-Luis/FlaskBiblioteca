from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme

from src.backend.extensions.admin.views import (
    AdminAccess,
    BookView,
    LendingView,
    LibrarianView,
)
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.models.book_loan import BookLoan
from src.backend.models.users import User

admin = Admin()


def admin_view_controller():
    """ModelView's anager"""
    admin_views = [
        admin.add_view(LibrarianView(User, db.session)),
        admin.add_view(
            BookView(Books, db.session, menu_icon_type="fa", menu_icon_value="fa-book")
        ),
        admin.add_view(LendingView(BookLoan, db.session, name="Empréstimo")),
    ]

    return admin_views


def admin_link_controller():
    """MenuLink's manager"""
    admin_link = [
        admin.add_link(
            MenuLink(
                name="Sair",
                endpoint="auth.logout",
                icon_type="fa",
                icon_value="fa-sign-out",
            )
        )
    ]
    return admin_link


def init_app(app):
    admin.init_app(
        app,
        index_view=AdminAccess(
            name="Home",
            endpoint=app.config["FLASK_ADMIN_ENDPOINT"],
            url=app.config["FLASK_ADMIN_URL"],
            # template="templates/admin",
        ),
    )
    admin.name = app.config["FLASK_ADMIN_TITLE"]
    admin.theme = Bootstrap4Theme(swatch="cerulean")
    admin_view_controller()
    admin_link_controller()
