from dynaconf import settings
from flask import redirect, request, url_for
from flask_admin.base import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from wtforms.fields import PasswordField

from src.backend.extensions.database import db
from src.backend.extensions.security import access_confirmation, generate_password
from src.backend.models.models import Role
from src.backend.services import book_services


class AdminAccess(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role(
            settings.ROLES[0]
        )

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))

    @expose("/")
    @login_required
    def index(self):
        books = book_services
        return self.render("admin/index.html", books=books, title="Admin Dashboard")


class LibrarianView(ModelView):
    form_columns = (
        "firstname",
        "lastname",
        "email",
        "password",
        "phone",
        "role",
    )

    column_list = ("fullname", "email", "phone", "is_confirmed", "role")

    form_extra_fields = {
         "password": PasswordField("Password")
    }

    form_args = {
        "role": {
            "query_factory": lambda: Role.query.all(),
            "default": lambda: Role.query.filter_by(type="librarian").first(),
        },
    }

    def on_model_change(self, form, model, is_created):
        model.fullname = f"{form.firstname.data} {form.lastname.data}"

        if form.password.data:
            model.password = generate_password(form.password.data)
        try:
            if is_created:
                access_confirmation(model)
        except Exception:
            db.session.rollback()
 