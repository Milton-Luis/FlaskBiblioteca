from datetime import datetime

from app.backend.services import book_services, lending_services
from flask import (
    flash,
    jsonify,
    logging,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.sql import asc, or_

from app.backend.extensions.database import db
from app.backend.model.models import Books, LendingBooks, Students, User

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
    # lending = LendingBooks()

    context = {}
    return render_template(
        "pages/index.html", books=books, lending=lending, title="Início"
    )


@main.route("/livros/", methods=["POST", "GET"])
@login_required
def view_books():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)
    books = (
        db.session.query(Books)
        .order_by(asc(Books.title))
        .paginate(page=page, per_page=10, error_out=True)
    )

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

    today = datetime.now().date()

    context = {
        "lends": lends,
        "endpoint": "main.lendings",
        "title": "Empréstimos",
        "today": today,
        "lendings": lending_services,
    }
    return render_template("pages/lendings.html", **context)


@main.route("/livros/novo/", methods=["GET", "POST"])
@login_required
def add_books():
    form = BookForm()
    if form.validate_on_submit():
        books = Books(
            title=form.title.data,
            author=form.author.data,
            total_of_books=form.quantity.data,
            available_quantity=form.quantity.data,
            isbn=form.isbn.data,
        )
        db.session.add(books)
        db.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))

    context = {"form": form, "title": "Novo Livro"}
    return render_template("pages/add_books.html", **context)


@main.route("/emprestimos/novo/<title>/buscar-locatario/", methods=["POST", "GET"])
@login_required
def search_borrower(title):
    search_form = SearchBookForm()
    get_book = db.session.query(Books).filter(Books.title == title).first()

    if search_form.search.data == "":
        flash("Digite o nome do locatário", "warning")
        return redirect(url_for("main.new_loan", title=title))

    if search_form.validate_on_submit():
        name = search_form.search.data
        get_user = (
            db.session.query(User).filter(User.fullname.ilike(f"%{name}%")).first()
        )
        if get_user:
            session["user_id"] = get_user.id
            # flash(f"Usuário encontrado - ID: {session.get('user_id')}", "success")
            return redirect(url_for("main.new_loan", title=title))
        else:
            flash("Nome não cadastrado", "warning")
            return redirect(url_for("main.new_loan", title=title))

    get_user = search_form.search.data
    render_template(
        "pages/new_lending.html",
        search_form=search_form,
        title="Novo Empréstimo",
        get_user=get_user,
        get_book=get_book,
    )


@main.route("/emprestimos/novo/<title>/", methods=["POST", "GET"])
@login_required
def new_loan(title):
    form = LendingBooksForm()
    search_form = SearchBookForm()

    get_user = db.session.query(User).filter(User.id == session.get("user_id")).first()
    get_book = db.session.query(Books).filter(Books.title == title).first()
    form.title.data = get_book.title

    if form.validate_on_submit():
        user_id = session.get("user_id")
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
                db.session.close()
                return redirect(url_for("main.index"))

        else:
            flash("Erro: ID do usuário não encontrado na sessão", "danger")

    context = {
        "form": form,
        "title": "Novo Empréstimo",
        "get_book": get_book,
        "get_user": get_user,
        "search_form": search_form,
    }
    return render_template("pages/new_lending.html", **context)


@main.route("/emprestimos/devolucao/<int:id>/", methods=["GET", "POST"])
@login_required
def return_book(id):
    lendings = db.session.query(LendingBooks).filter_by(book_id=id).first()
    book = lendings.books

    book_services.add_available_quantity(book.id, lendings.quantity_lent)

    db.session.delete(lendings)
    db.session.commit()

    flash("Livro devolvido com sucesso!", "success")
    return redirect(url_for("main.index"))
