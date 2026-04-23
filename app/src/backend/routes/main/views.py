from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import asc

from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.models.loan import BookLoan
from src.backend.models.reader import Reader
from src.backend.services import book_service, reader_service, loan_service

from . import main
from .forms import BookForm, BookLoanForm, ReaderForm, SearchBookForm


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


@main.route("/leitor/novo", methods=["POST", "GET"])
@login_required
def new_reader():
    form = ReaderForm()

    if form.validate_on_submit():
        try:
            reader_service.create_reader(form)
            db.session.commit()

            flash("Novo leitor adicionado!!", "success")
        except Exception:
            db.session.rollback()
            flash("Erro ao adicionar informações", "danger")
        return redirect(url_for("main.index"))

    return render_template(
        "pages/new_reader.html", form=form, title="Adicionar novo Leitor"
    )


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


@main.route("/livros/detalhes/<slug>", methods=["GET", "POST"])
@login_required
def book_details(slug):
    book = Books.query.filter_by(slug=slug).first()

    return render_template(
        "pages/book_detail.html", book=book, title=f"Livro - {book.title}"
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
        except Exception:
            db.session.rollback()
            flash("Erro ao criar novo livro!", "danger")

        return redirect(url_for("main.index"))

    return render_template("pages/new_book.html", form=form, title="Novo Livro")


@main.route("/emprestimos")
@login_required
def loans_page():
    page = request.args.get("page", 1, type=int)
    loans = BookLoan.query.paginate(page=page, per_page=5, error_out=True)

    return render_template(
        "pages/loans.html",
        loans=loans,
        endpoint="main.loans",
        title="Empréstimos",
    )


@main.route("/emprestimos/novo/<slug>", methods=["POST", "GET"])
@login_required
def new_loan(slug):
    session_id = session.get("reader_id")

    form = BookLoanForm()
    search_form = SearchBookForm()

    reader = db.session.query(Reader).filter_by(id=session_id).first()
    book = db.session.query(Books).filter_by(slug=slug).first()

    form.title.data = book.title
    if session_id:
        if not reader:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("main.new_loan", slug=book.slug))

        if loan_service.has_active_loan(session_id, book.id):
            flash(
                f"{reader.fullname} já possui um empréstimo ativo para este livro.",
                "warning",
            )
            return redirect(url_for("main.new_loan", slug=book.slug))

    if form.validate_on_submit():
        if not session_id or not reader:
            flash("Selecione um usuário para realizar o empréstimo.", "warning")
            return redirect(url_for("main.new_loan", slug=book.slug))
        try:
            loan_service.create_loan(form, session_id, book.id)
            book_service.borrow_book(book.id)

            db.session.commit()
            flash("Empréstimo realizado!", "success")
        except ValueError as e:
            db.session.rollback()
            flash(f"Erro ao criar empréstimo: {str(e)}", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"{reader.fullname} já alugou um livro. ", "danger")
            print(f"Erro ao criar empréstimo: {e}")

        session.pop("reader_id")
        return redirect(url_for("main.index"))

    return render_template(
        "pages/new_loan.html",
        form=form,
        book=book,
        reader=reader,
        search_form=search_form,
        title="Novo Empréstimo",
    )


@main.route("/emprestimos/devolucao/<slug>", methods=["GET", "POST"])
@login_required
def return_book(slug):
    loans = db.session.query(BookLoan).join(Books).filter_by(slug=slug).first()

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
        loan_service.create_loan(loan, loan.reader_id, loan.book_id)
        db.session.commit()
        flash("Empréstimo renovado com sucesso!", "success")
    else:
        flash("Empréstimo não encontrado.", "danger")

    return redirect(url_for("main.loans"))
