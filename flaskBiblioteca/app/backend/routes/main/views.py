from app.backend.extensions.database import db
from app.backend.model.models import Books, LendingBooks
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import main
from .forms import BookForm, LendingForm, SearchBookForm


@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))

    book = Books()

    context = {"book": book, "title": "Início"}
    return render_template("pages/index.html", **context)


@main.route("/livros/", methods=["POST", "GET"])
@login_required
def books():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)

    books = db.session.query(Books).paginate(page=page, per_page=10, error_out=True)

    context = {
        "books": books,
        "endpoint": "main.books",
        "form": form,
        "title": "Livros",
    }
    return render_template("pages/books.html", **context)


@main.route("/livros/detalhes/<int:book_id>/", methods=["GET", "POST"])
@login_required
def book_details(book_id):
    book = db.session.get(Books, book_id)

    context = {"book": book, "title": f"Livro - {book.title}"}
    return render_template("pages/book_detail.html", **context)


@main.route("/emprestimos/")
@login_required
def lendings():
    loans = (
        db.session.query(Books)
        .filter(Books.title)
        .paginate(page=1, per_page=5, error_out=True)
    )

    context = {
        "loans": loans,
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


@main.route("/emprestimos/novo/", methods=["GET", "POST"])
@login_required
def new_loan():
    form = LendingForm()
    if form.validate_on_submit():
        # get_book = Services.get_one_record(Book, Book.id)

        # get_user = Services.get_first_record(User, User.firstname)

        lending = LendingForm(
            quantityBooks=form.quantity.data,
            loan_date=form.loan_date.data,
            return_date=form.return_date.data,
            users=User()
        )
        lending.save()

        flash("Empréstimo realizado!", "success")
        return redirect(url_for("main.index"))

    context = {
        "form": form,
        "title": "Novo Empréstimo",
    }
    return render_template("pages/new_lending.html", **context)
