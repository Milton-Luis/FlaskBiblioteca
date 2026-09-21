from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required
from src.backend.extensions.database import db
from src.backend.routes.main import main
from src.backend.routes.main.forms import BookLoanForm, SearchForm
from src.backend.services import book_service, loan_service, reader_service


@main.route("/emprestimos")
@login_required
def loans_page():
    loans = db.paginate(
        loan_service.get_all_loans(), per_page=5, max_per_page=10, error_out=True
    )

    return render_template(
        "pages/loans.html",
        loans=loans,
        title="Empréstimos",
    )


@main.route("/emprestimos/novo/", methods=["POST", "GET"])
@login_required
def new_loan():
    loan_form = BookLoanForm()
    search_form = SearchForm()

    slug = request.args.get("slug")

    reader_id = session.get("reader_id")
    reader = reader_service.get_valid_reader(reader_id)

    book = None
    if slug:
        book = book_service.get_book_by_slug(slug)
        loan_form.title.data = book.title

    if loan_form.validate_on_submit():
        try:
            if loan_service.has_active_loan(reader.id):
                flash("Leitor já possui um empréstimo ativo.", "warning")

            loan_service.create_loan(loan_form, reader, book)
            db.session.commit()
            flash("Empréstimo realizado!", "success")

        except ValueError as error:
            db.session.rollback()
            raise error from ValueError

        session.pop("reader_id")
        return redirect(url_for("main.index"))

    return render_template(
        "pages/new_loan.html",
        search_form=search_form,
        loan_form=loan_form,
        book=book,
        reader=reader,
        title="Novo Empréstimo",
    )


@main.route("/emprestimos/devolucao/<slug>", methods=["GET", "POST"])
@login_required
def return_loan(slug):
    loans = loan_service.get_loan_by_book_slug(slug)

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
# @main.route("/emprestimos/renovar/<int:id>/", methods=["GET", "POST"])
# @login_required
# def renew_loan(id):
#     search_form = SearchForm()
#     reader_id = session.get("reader_id")

#     loan = db.session.get(BookLoan, id)
#     reader = reader_service.get_valid_reader(reader_id)

#     search_form.search.data = reader.fullname

#     if loan:
#         loan_service.create_loan(loan, reader, loan.book_id)
#         db.session.commit()
#         flash("Empréstimo renovado com sucesso!", "success")
#     else:
#         flash("Empréstimo não encontrado.", "danger")

#     return redirect(url_for("main.loans"))
