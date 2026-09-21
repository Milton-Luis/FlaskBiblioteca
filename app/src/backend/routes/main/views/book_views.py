from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from src.backend.extensions.database import db
from src.backend.routes.main import main
from src.backend.routes.main.forms import BookForm, SearchForm
from src.backend.services import book_service
from sqlalchemy.exc import SQLAlchemyError


@main.route("/livros", methods=["POST", "GET"])
@login_required
def books_page():
    form = SearchForm()
    books = db.paginate(book_service.get_all_books(), per_page=2, max_per_page=10)

    return render_template(
        "pages/books.html",
        books=books,
        form=form,
        title="Livros",
    )


@main.route("/livros/novo", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        try:
            book_service.create_book(form)
            db.session.commit()

        except SQLAlchemyError as error:
            db.session.rollback()
            flash("Erro ao criar novo livro!", "danger")
            raise error
        else:
            flash("Livro adicionado com sucesso!", "success")
            return redirect(url_for("main.index"))

    return render_template("pages/new_book.html", form=form, title="Novo Livro")


@main.route("/livros/detalhes/<slug>", methods=["GET", "POST"])
@login_required
def book_details(slug):
    book = book_service.get_book_by_slug(slug)

    return render_template(
        "pages/book_detail.html", book=book, title=f"Livro - {book.title}"
    )
