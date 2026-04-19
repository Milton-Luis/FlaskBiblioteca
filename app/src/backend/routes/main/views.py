from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import asc

from src.backend.services import loan_service
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.models.book_loan import BookLoan
from src.backend.models.users import User
from src.backend.services import book_service
from src.backend.utils.utils import get_formated_date

from . import main
from .forms import BookForm, BookLoanForm, SearchBookForm


@main.before_app_request
def before_app_request():
    ...
    # return loan_services.send_notification_of_return_book()


@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))

    books = book_service
    loan = loan_service

    return render_template("pages/index.html", title="Início", books=books, loan=loan)


@main.route("/livros", methods=["POST", "GET"])
@login_required
def books_page():
    form = SearchBookForm()

    page = request.args.get("page", 1, type=int)
    books = Books.query.order_by(asc(Books.title)).paginate(
        page=page, per_page=10, error_out=True
    )

    return render_template(
        "pages/books.html",
        books=books,
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
        book_service.create_book(form)

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("main.index"))

    return render_template("pages/add_books.html", form=form, title="Novo Livro")


@main.route("/emprestimos/")
@login_required
def loans_page():
    page = request.args.get("page", 1, type=int)
    lends = BookLoan.query.paginate(page=page, per_page=5, error_out=True)

    borrow_date = get_formated_date(lends.items[0].loan_date) if lends.items else "N/A"
    return_date = (
        get_formated_date(lends.items[0].return_date) if lends.items else "N/A"
    )

    today = datetime.now().date()

    return render_template(
        "pages/loans.html",
        lends=lends,
        endpoint="main.loans",
        today=today,
        borrow_date=borrow_date,
        return_date=return_date,
        title="Empréstimos",
    )


@main.route("/emprestimos/novo/<slug>/", methods=["POST", "GET"])
@login_required
def new_loan(slug):
    session_id = session.get("user_id")

    form = BookLoanForm()
    search_form = SearchBookForm()

    user = User.query.filter_by(id=session_id).first()
    book = db.session.query(Books).filter_by(slug=slug).first()

    form.title.data = book.title
    if session_id:
        if not user:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("main.new_loan", slug=book.slug))

        if loan_service.has_active_loan(session_id, book.id):
            flash(
                f"{user.fullname} já possui um empréstimo ativo para este livro.",
                "warning",
            )
            return redirect(url_for("main.new_loan", slug=book.slug))

    if form.validate_on_submit():
        if not session_id or not user:
            flash("Selecione um usuário para realizar o empréstimo.", "warning")
            return redirect(url_for("main.new_loan", slug=book.slug))
        try:
            loan_service.create_loan(form, user.id, book.id)
            book_service.borrow_book(book.id)

            db.session.commit()
            flash("Empréstimo realizado!", "success")
        except ValueError as e:
            db.session.rollback()
            flash(f"Erro ao criar empréstimo: {str(e)}", "danger")
        except Exception:
            db.session.rollback()
            flash(f"{user.fullname} já alugou um livro.", "danger")

        session.pop("user_id")
        return redirect(url_for("main.new_loan", slug=book.slug))

    return render_template(
        "pages/new_loan.html",
        form=form,
        book=book,
        user=user,
        search_form=search_form,
        title="Novo Empréstimo",
    )


@main.route("/emprestimos/novo/<slug>/buscar-locatario/", methods=["POST", "GET"])
@login_required
def search_borrower(slug):
    search_form = SearchBookForm()
    book = db.session.query(Books).filter_by(slug=slug).first()

    if search_form.search.data == "":
        flash("Digite o nome do locatário", "warning")
        return redirect(url_for("main.new_loan", slug=book.slug))

    if search_form.validate_on_submit():
        name = search_form.search.data
        user = db.session.query(User).filter(User.fullname.ilike(f"%{name}%")).first()

        if user:
            session["user_id"] = user.id
            flash("Usuário encontrado", "success")
            return redirect(url_for("main.new_loan", slug=book.slug))
        else:
            flash("Nome não cadastrado", "warning")
            return redirect(url_for("main.new_loan", slug=book.slug))

    user = search_form.search.data

    return render_template(
        "pages/new_loan.html",
        search_form=search_form,
        title="Novo Empréstimo",
        user=user,
        book=book,
    )


@main.route("/emprestimos/devolucao/<int:id>/", methods=["GET", "POST"])
@login_required
def return_book(id):
    loans = db.session.query(BookLoan).filter_by(book_id=id).first()

    book_service.return_book(loans.book_id)

    db.session.delete(loans)
    db.session.commit()

    flash("Livro devolvido com sucesso!", "success")
    return redirect(url_for("main.index"))


@main.route("/emprestimos/renovar/<int:id>/", methods=["GET", "POST"])
@login_required
def renew_loan(id):
    loan = db.session.query(BookLoan).filter_by(id=id).first()

    if loan:
        loan_service.create_loan(loan, loan.user_id, loan.book_id)
        db.session.commit()
        flash("Empréstimo renovado com sucesso!", "success")
    else:
        flash("Empréstimo não encontrado.", "danger")

    return redirect(url_for("main.loans"))
