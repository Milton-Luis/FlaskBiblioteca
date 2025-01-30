from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.backend.model.models import Books, LendingBooks, User

from . import main
from .forms import LendingForm, NewBookForm, SearchBookForm
from app.backend.extensions.database import db

@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))
    return render_template("pages/index.html", title="Início")


@main.route("/livros/", methods=["POST", "GET"])
@login_required
def books():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)

    books = db.session.query(Books).filter(Books.title).paginate(
        page=page, per_page=10, error_out=True
    )
    return render_template(
        "pages/books.html",
        books=books,
        endpoint="main.books",
        form=form,
        title="Livros",
    )


@main.route("/livros/<int:book_id>/", methods=["GET", "POST"])
@login_required
def showBook(book_id):
    book = db.session.query(Books).get(book_id)
    return render_template(
        "pages/showbook.html",
        book=book,
        title=f"Livro - {book.title}",
    )


@main.route("/emprestimos/")
@login_required
def loanBooks():
    loans = db.session.query(Books).filter(Books.title).paginate(
        page=1, per_page=5, error_out=True
    )

    return render_template(
        "pages/loanBooks.html",
        loans=loans,
        endpoint="main.loanBooks",
        title="Empréstimos",
    )


@main.route("/livros/novo/", methods=["GET", "POST"])
@login_required
def new_book():
    form = NewBookForm()
    if form.validate_on_submit():
        books = Books(
            title=form.title.data,
            author=form.author.data,
            quantity_of_books=form.quantity.data,
            isbn=form.isbnCode.data,
        )
        db.session.add(books)
        db.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))
    return render_template("pages/newBook.html", form=form, title="Novo Livro")


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
        )
        lending.save()

        flash("Empréstimo realizado!", "success")
        return redirect(url_for("main.index"))
    return render_template(
        "pages/newLoan.html", form=form, title="Novo empréstimo"
    )
