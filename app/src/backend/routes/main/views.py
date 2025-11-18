from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import asc

from src.backend.extensions.database import db
from src.backend.models.models import Books, LendingBooks, User
from src.backend.services import book_services, lending_services
from src.backend.utils.utils import slugfy

from . import main
from .forms import BookForm, LendingBooksForm, SearchBookForm


@main.before_app_request
def before_app_request():
    ...
    # return lending_services.send_notification_of_return_book()


@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))

    books = book_services
    lending = lending_services

    return render_template(
        "pages/index.html", title="Início", books=books, lending=lending
    )


@main.route("/livros", methods=["POST", "GET"])
@login_required
def view_books():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)
    books = Books.query.order_by(asc(Books.title)).paginate(
        page=page, per_page=10, error_out=True
    )

    return render_template(
        "pages/books.html",
        books=books,
        endpoint=main.books,
        form=form,
        title="Livros",
    )


@main.route("/livros/detalhes/<slug>", methods=["GET", "POST"])
@login_required
def book_details(slug):
    book = Books.query.filter_by(slug=slug).first()

    return render_template(
        "pages/book_detail.html", book=book, title=f"Livro - {book.title}"
    )


@main.route("/livros/novo", methods=["GET", "POST"])
@login_required
def add_books():
    form = BookForm()
    if form.validate_on_submit():
        books = Books(
            title=form.title.data,
            slug=slugfy(form.title.data),
            author=form.author.data,
            total_of_books=form.quantity.data,
            available_quantity=form.quantity.data,
            isbn=form.isbn.data,
        )
        db.session.add(books)
        db.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))

    return render_template("pages/add_books.html", form=form, title="Novo Livro")


@main.route("/emprestimos/")
@login_required
def lendings():
    page = request.args.get("page", 1, type=int)
    lends = LendingBooks.query.paginate(page=page, per_page=5, error_out=True)

    today = datetime.now().date()

    return render_template(
        "pages/lendings.html",
        lends=lends,
        endpoint=main.lendings,
        today=today,
        lendings=lending_services,
        title="Empréstimos",
    )


@main.route("/emprestimos/novo/<slug>/", methods=["POST", "GET"])
@login_required
def new_loan(slug):
    session_id = session.get("user_id")

    form = LendingBooksForm()
    search_form = SearchBookForm()

    get_user = User.query.filter_by(id == session_id).first()
    get_book = Books.query.filter_by(slug == slug).first()
    form.slug.data = get_book.slug

    if form.validate_on_submit():
        user_id = session_id
        if user_id:
            return_date_with_time = datetime.combine(
                form.return_date.data, datetime.now().time()
            )

            lending = LendingBooks(
                lending_date=datetime.now(),
                return_date=return_date_with_time,
                quantity_lent=form.quantity.data,
                user_id=user_id,
                book_id=get_book.id,
            )
            try:
                db.session.add(lending)

                book_services.subtract_available_quantity(
                    get_book.id, lending.quantity_lent
                )
                db.session.commit()
                flash("Empréstimo realizado!", "success")

                session.pop("user_id")

            except Exception:
                session.pop("user_id")
                db.session.rollback()
                flash(
                    f"O Locatário {get_user.fullname} já alugou um livro. A devolução é no dia {lending_services.get_formated_date(lending.return_date)}!",
                    "danger",
                )

            finally:
                return redirect(url_for("main.index"))

        else:
            flash("Erro: ID do usuário não encontrado na sessão", "danger")

    return render_template(
        "pages/new_lending.html",
        form=form,
        get_book=get_book,
        get_user=get_user,
        search_form=search_form,
        title="Novo Empréstimo",
    )


@main.route("/emprestimos/novo/<slug>/buscar-locatario/", methods=["POST", "GET"])
@login_required
def search_borrower(slug):
    search_form = SearchBookForm()
    books = Books.query.filter(Books.slug == slug).first()

    if search_form.search.data == "":
        flash("Digite o nome do locatário", "warning")
        return redirect(url_for("main.new_loan", title=books.title))

    if search_form.validate_on_submit():
        name = search_form.search.data
        users = User.query.filter(User.fullname.ilike(f"%{name}%")).first()
        if users:
            session["user_id"] = users.id
            # flash(f"Usuário encontrado - ID: {session.get('user_id')}", "success")
            return redirect(url_for("main.new_loan", title=books.title))
        else:
            flash("Nome não cadastrado", "warning")
            return redirect(url_for("main.new_loan", title=books.title))

    users = search_form.search.data
    render_template(
        "pages/new_lending.html",
        search_form=search_form,
        title="Novo Empréstimo",
        users=users,
        books=books,
    )


@main.route("/emprestimos/devolucao/<int:id>/", methods=["GET", "POST"])
@login_required
def return_book(id):
    lendings = LendingBooks.query.filter_by(book_id=id).first()
    book = lendings.books

    book_services.add_available_quantity(book.id, lendings.quantity_lent)

    db.session.delete(lendings)
    db.session.commit()

    flash("Livro devolvido com sucesso!", "success")
    return redirect(url_for("main.index"))
