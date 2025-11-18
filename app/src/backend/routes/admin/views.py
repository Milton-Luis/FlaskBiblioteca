from flask import abort, current_app, flash, redirect, url_for
from flask_admin.base import AdminIndexView, expose
from flask_login import current_user, login_required

from src.backend.extensions.database import db
from src.backend.extensions.security import access_confirmation, generate_password
from src.backend.models.models import Librarian, User
from src.backend.routes.auth.forms import AddLibrarianForm
from src.backend.services import book_services


class AdminAccess(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        role = getattr(current_user, "role", None)

        if role is None:
            return False

        return getattr(role, "is_admin", False)
        # if current_user.roles.type == current_app.config["FLASK_ADMIN_ACCESS"]:
        #     return super().is_accessible()
        # else:
        #     return abort(403)

    def inaccessible_callback(self, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        return abort(403)

    @expose("/")
    @login_required
    def index(self):
        books = book_services
        return self.render("admin/index.html", books=books, title="Admin Dashboard")

    @expose("/new-register/", methods=["GET", "POST"])
    @login_required
    def add_librarian(self):
        form = AddLibrarianForm()

        if form.validate_on_submit():
            librarian = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                phone=form.phone.data,
                roles=Librarian(
                    rolename=current_app.config["ROLE_PREFIX"],
                    password=generate_password(form.password.data),
                ),
            )
            db.session.add(librarian)
            db.session.commit()

            access_confirmation(librarian)

            flash("Inserido com sucesso", "success")
            return redirect(url_for("admin.index"))
        return self.render("admin/librarian.html", form=form, title="New Register")
