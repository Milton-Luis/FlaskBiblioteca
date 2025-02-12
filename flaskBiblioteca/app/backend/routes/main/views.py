from datetime import datetime
from app.backend.extensions.database import db
from app.backend.model.models import Books, LendingBooks, Students, User

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import asc, or_

from . import main
from .forms import BookForm, LendingBooksForm, SearchBookForm


@main.before_app_request
def before_app_request():
    lending = LendingBooks()

    return lending.send_notification_of_return_book()


@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))

    books = Books()
    lending = LendingBooks()

    context = {"books": books, "lending": lending, "title": "Início"}
    return render_template("pages/index.html", **context)


@main.route("/livros/", methods=["POST", "GET"])
@login_required
def books():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)
    books = (
        db.session.query(Books)
        .order_by(asc(Books.title))
        .paginate(page=page, per_page=3, error_out=True)
    )

    if form.validate_on_submit():
        search = form.search.data
        books = (
            db.session.query(Books)
            .filter(
                or_(
                    Books.title.like(f"%{search}%"),
                    Books.author.startswith(f"{search}"),
                )
            )
            .order_by(asc(Books.title))
            .paginate(page=page, per_page=3, error_out=True)
        )
        print(form.errors)

    context = {
        "books": books,
        "endpoint": "main.books",
        "form": form,
        "title": "Livros",
    }
    return render_template("pages/books.html", **context)


@main.route("/livros/detalhes/<title>/", methods=["GET", "POST"])
@login_required
def book_details(title):
    book = db.session.query(Books).filter_by(title=title).first()

    context = {"book": book, "title": f"Livro - {title}"}
    return render_template("pages/book_detail.html", **context)


@main.route("/emprestimos/")
@login_required
def lendings():
    page = request.args.get("page", 1, type=int)
    lends = db.session.query(LendingBooks).paginate(
        page=page, per_page=5, error_out=True
    )

    context = {
        "lends": lends,
        "endpoint": "main.lendings",
        "title": "Empréstimos",
    }
    return render_template("pages/lendings.html", **context)


@main.route("/livros/novo/", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        books = Books(
            title=form.title.data,
            author=form.author.data,
            quantity_of_books=form.quantity.data,
            isbn=form.isbn.data,
        )
        db.session.add(books)
        db.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))

    context = {"form": form, "title": "Novo Livro"}
    return render_template("pages/new_book.html", **context)


@main.route("/emprestimos/novo/<title>/", methods=["POST", "GET"])
@login_required
def new_loan(title):
    form = LendingBooksForm()

    # Corrigir a parte do usuário que não está retornando corretamente
    get_book = db.session.query(Books).filter(Books.title == title).first()
    get_user = db.session.query(User)

    form.title.data = get_book.get_title()

    for user in get_user:
        for student in user.students:
            form.course.data = student.get_course()

    if form.validate_on_submit():
        fullname = form.borrower.data
        get_user = (
            db.session.query(User).filter(User.firstname.ilike(f"%{fullname}")).first()
        )

        if not get_user:
            flash("Nome não cadastrado", "warning")
            return redirect(url_for("main.new_loan", title=title))

        lending = LendingBooks(
            lending_date=datetime.now(),
            return_date=form.return_date.data,
            quantity_lent=form.quantity.data,
            user_id=get_user.id,
            book_id=get_book.id,
        )
        try:
            db.session.add(lending)
            db.session.commit()
        except Exception as e:
            flash(f"Erro ao criar empréstimo! {e}", "danger")
            db.session.rollback()
        else:
            flash("Empréstimo realizado!", "success")
            return redirect(url_for("main.index"))
    else:
        print(form.errors)

    context = {
        "form": form,
        "title": "Novo Empréstimo",
        "get_user": get_user,
        "get_book": get_book,
    }
    return render_template("pages/new_lending.html", **context)


# fazer join de student para user
