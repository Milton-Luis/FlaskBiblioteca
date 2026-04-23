# from src.backend.services import book_services
from datetime import datetime, timedelta

from dynaconf import settings
from flask import redirect, request, url_for
from flask_admin.base import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from wtforms.fields import PasswordField

from src.backend.extensions.database import db
from src.backend.extensions.security import access_confirmation, generate_password
from src.backend.utils.utils import slugfy

from src.backend.models.roles import Roles


class AdminAccess(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role(
            settings.ROLES["admin"]
        )

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))


class DashboardView(BaseView):
    @expose("/")
    @login_required
    def index(self):
        return self.render(
            "admin/index.html",
            livros_populares=[],
            atrasados=[],
            devolucoes_hoje=[],
            current_year=datetime.now().year,
        )


class LibrarianView(ModelView):
    form_columns = (
       
        "email",
        "password",
        "role",
    )

    column_list = ( "email", "role", "is_confirmed")

    column_labels = {
        "email": "Email",
        "is_confirmed": "Confirmado?",
        "role": "Atividade",
    }

    form_extra_fields = {"password": PasswordField("Password")}

    form_args = {
        "role": {
            "query_factory": lambda: Roles.query.all(),
            "default": lambda: Roles.query.filter_by(type="librarian").first(),
        },
    }

    def on_model_change(self, form, model, is_created):

        if form.password.data:
            model.password = generate_password(form.password.data)
        try:
            if is_created:
                access_confirmation(model)
        except Exception:
            db.session.rollback()


class BookView(ModelView):
    form_excluded_columns = ("available_quantity",)
    form_columns = ("title", "author", "isbn", "total_of_books")
    column_labels = {
        "title": "Título",
        "author": "Autor",
        "isbn": "ISBN",
        "total_of_books": "Quantidade em estoque",
        "available_quantity": "Disponível para empréstimo",
    }

    def on_model_change(self, form, model, is_created):
        model.title = form.title.data.capitalize()
        model.author = form.author.data.title()
        model.slug = slugfy(model.title)
        model.available_quantity = model.total_of_books

        return super().on_model_change(form, model, is_created)


class LoanView(ModelView):
    ...
    form_columns = ["reader", "book", "loan_date", "return_date"]
    column_labels = {
        "reader": "Leitor(a)",
        "book": "Livro",
        "loan_date": "Data do empréstimo",
        "return_date": "Data de devolução",
    }

    # form_args = {
    #     "loan_date": {"format": "%d/%m/%Y"},
    #     "return_date": {"format": "%d/%m/%Y"},
    # }

    def create_form(self, obj=None):
        form = super().create_form(obj)

        now = datetime.now()

        if not form.loan_date.data:
            form.loan_date.data = now

        if not form.return_date.data:
            form.return_date.data = now + timedelta(days=7)

        return form

    def on_model_change(self, form, model, is_created):
        print("MODEL:", model)
        print("IS CREATED:", is_created)


# """SAWarning: Column 'loan_book.id' is marked as a member of the primary key for table 'loan_book', but has no Python-side or server-side default generator indicated, nor does it indicate 'autoincrement=True' or 'nullable=True', and no explicit value is passed.  Primary key columns typically may not store NULL. Note that as of SQLAlchemy 1.1, 'autoincrement=True' must be indicated explicitly for composite (e.g. multicolumn) primary keys if AUTO_INCREMENT/SERIAL/IDENTITY behavior is expected for one of the columns in the primary key. CREATE TABLE statements are impacted by this change as well on most backends.
#   self.session.commit()"""
