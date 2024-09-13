from app.backend.model.models import Book, LoanBooks, User
from app.backend.utils.operations import Services
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import main
from .forms import AddBookForm, AddLoanForm, SearchBookForm


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

    books = Services.get_all_records(Book, Book.title).paginate(
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
    book = Services.get_one_record(Book, book_id)
    return render_template(
        "pages/showbook.html",
        book=book,
        title=f"Livro - {book.title}",
    )


@main.route("/emprestimos/")
@login_required
def loanBooks():
    loans = Services.get_all_records(Book, Book.title).paginate(
        page=1, per_page=5, error_out=True
    )

    return render_template(
        "pages/loanBooks.html",
        loans=loans,
        endpoint="main.loanBooks",
        title="Empréstimos",
    )


@main.route("/livros/novo/livro", methods=["GET", "POST"])
@login_required
def new_book():
    form = AddBookForm()
    if form.validate_on_submit():
        Services.new_register(
            Book,
            form.title.data.form.author.data,
            form.quantityBooks.data,
            form.isbnCode.data,
        )
        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))
    return render_template("pages/newBook.html", form=form, title="Novo Livro")


@main.route("/emprestimos/novo/emprestimo/", methods=["GET", "POST"])
@login_required
def new_loan():
    form = AddLoanForm()
    if form.validate_on_submit():
        get_book = Services.get_one_record(Book, Book.id)

        get_user = Services.get_first_record(User, User.firstname)

        Services.new_register(
            LoanBooks,
            quantityBooks=form.quantity.data,
            loan_date=form.loan_date.data,
            return_date=form.return_date.data,
            user_id=get_user.id,
            book_id=get_book.id,
        )

        flash("Empréstimo realizado!", "success")
        return redirect(url_for("main.index"))
    return render_template(
        "pages/newLoan.html", form=form, get_book=get_book, title="Novo empréstimo"
    )
