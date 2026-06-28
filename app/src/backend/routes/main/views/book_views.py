from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import asc
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.routes.main import main
from src.backend.routes.main.forms import BookForm, SearchBookForm
from src.backend.services import book_service


@main.route("/livros", methods=["POST", "GET"])
@login_required
def books_page():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)
    books = (
        db.session.query(Books)
        .order_by(asc(Books.title))
        .paginate(page=page, per_page=10, error_out=True)
    )

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

            flash("Livro adicionado com sucesso!", "success")
            return redirect(url_for("main.index"))
        except Exception:
            db.session.rollback()
            flash("Erro ao criar novo livro!", "danger")

    return render_template("pages/new_book.html", form=form, title="Novo Livro")


@main.route("/livros/detalhes/<slug>", methods=["GET", "POST"])
@login_required
def book_details(slug):
    book = Books.query.filter_by(slug=slug).first()

    return render_template(
        "pages/book_detail.html", book=book, title=f"Livro - {book.title}"
    )
