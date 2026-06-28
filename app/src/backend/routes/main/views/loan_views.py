from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.models.loan import BookLoan
from src.backend.models.reader import Reader
from src.backend.routes.main import main
from src.backend.routes.main.forms import BookLoanForm, SearchBookForm
from src.backend.services import book_service, loan_service


@main.route("/emprestimos")
@login_required
def loans_page():
    page = request.args.get("page", 1, type=int)
    loans = BookLoan.query.paginate(page=page, per_page=5, error_out=True)

    return render_template(
        "pages/loans.html",
        loans=loans,
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

        if loan_service.has_active_loan(session_id):
            flash(
                f"{reader.fullname} já possui um empréstimo ativo.",
                "warning",
            )
            session.pop("reader_id")
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
        except Exception:
            db.session.rollback()
            flash(f"{reader.fullname} já alugou um livro. ", "danger")

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

    try:
        book_service.return_book(loans.book_id)

        db.session.delete(loans)
        db.session.commit()

        flash("Livro devolvido com sucesso!", "success")
    except ValueError as e:
        db.session.rollback()
        flash(f"Erro ao devolver livro: {str(e)}", "danger")
    except Exception:
        db.session.rollback()
        flash("Erro ao processar devolução!", "danger")
    return redirect(url_for("main.index"))

# TODO ajustar a tora renew loan com tratamento de exceções e rollback
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
