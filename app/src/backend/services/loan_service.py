from datetime import datetime
from src.backend.extensions.database import db
from src.backend.models.loan import BookLoan
from src.backend.components.components import STATUS_MAPPING


def create_loan(form, reader_id: int, book_id: int) -> BookLoan:
    loan = BookLoan(
        reader_id=reader_id,
        book_id=book_id,
        loan_date=datetime.now(),
        due_date=datetime.combine(form.due_date.data, datetime.now().time()),
    )

    db.session.add(loan)

    return loan


def count_delayed_loans() -> int:
    return (
        db.session.query(BookLoan)
        .filter(BookLoan.status == STATUS_MAPPING["overdue"])
        .count()
    )


def count_books_due_today() -> int:
    return (
        db.session.query(BookLoan)
        .filter(BookLoan.status == STATUS_MAPPING["due_today"])
        .count()
    )


def has_active_loan(reader_id: int):
    """Verifica se o usuário já possui um empréstimo ativo para o mesmo livro."""
    return (
        db.session.query(BookLoan)
        .filter_by(reader_id=reader_id, return_date=None)
        .first()
        is not None
    )


def count_monthly_returns() -> int:
    today = datetime.now()
    first_day = datetime(today.year, today.month, 1)

    if today.month == 12:
        next_month = datetime(today.year + 1, 1, 1)
    else:
        next_month = datetime(today.year, today.month + 1, 1)

    return (
        db.session.query(BookLoan)
        .filter(BookLoan.due_date >= first_day)
        .filter(BookLoan.due_date < next_month)
        .filter(BookLoan.return_date is None)  # só se quiser pendentes
        .count()
    )
