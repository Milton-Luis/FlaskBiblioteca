from app.backend.extensions.database import db
from app.backend.model.models import Librarian, Role, Students, User
from app.backend.routes.admin.views import (AdminAccess, RoleModelView,
                                            StudentModelView, UserModelView)
from flask_admin import Admin
from flask_admin.menu import MenuLink

admin = Admin(base_template="admin/base.html", name="Biblioteca", template_mode="bootstrap3", index_view=AdminAccess())


def admin_view_controller():
    """manager of ModelViews"""
    admin_views = [
        admin.add_view(
            UserModelView(User, db.session, name="usuarios", category="Usuários")
        ),
        admin.add_view(
            RoleModelView(Role, db.session, name="perfis", category="Usuários")
        ),
        admin.add_view(
            StudentModelView(Students, db.session, name="estudantes", category="Usuários")
        ),
        admin.add_link(MenuLink(name="Sair", url="/logout"))
    ]
    return admin_views


def init_app(app):
    admin.init_app(app)
    admin_view_controller()
    admin.name = app.config["FLASK_ADMIN_TITLE"]
    admin.template_mode = app.config["FLASK_ADMIN_TEMPLATE"]
