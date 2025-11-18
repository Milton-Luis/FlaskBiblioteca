from flask_admin import Admin

from src.backend.routes.admin.views import AdminAccess

admin = Admin()


def admin_view_controller():
    """manager of ModelViews"""
    admin_views = []
    return admin_views


def init_app(app):
    admin.init_app(app, index_view=AdminAccess(name="Home", template="templates/admin"))
    admin_view_controller()
    admin.name = app.config["FLASK_ADMIN_TITLE"]
    admin.template_mode = app.config["FLASK_ADMIN_TEMPLATE"]
