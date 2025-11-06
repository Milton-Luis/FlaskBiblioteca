from flask import abort, current_app, flash, redirect, url_for
from flask_admin.base import AdminIndexView, expose
from flask_login import current_user, login_required

from app.backend.extensions.database import db
from app.backend.extensions.security import (access_confirmation,
                                             generate_password)
from app.backend.model.models import Librarian, Students, User
from app.backend.routes.auth.forms import AddLibrarianForm, AddStudentForm
from app.backend.services import book_services


class AdminAccess(AdminIndexView):
    def is_accessible(self):
        """
        Checks if the current user has admin access, otherwise, abort the access
        """
        if current_user.roles.type == current_app.config["FLASK_ADMIN_ACCESS"]:
            return super().is_accessible()
        else:
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

    @expose("/new-student/", methods=["POST", "GET"])
    @login_required
    def add_student(self):
        form = AddStudentForm()

        if form.validate_on_submit():
            student = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                phone=form.phone.data,
                student=[
                    Students(classroom=form.classroom.data, grade=form.grade.data)
                ],
            )
            db.session.add(student)
            db.session.commit()

            flash("Inserido com sucesso", "success")
            return redirect(url_for("admin.index"))
        return self.render("admin/addStudent.html", form=form, title="New Register")
