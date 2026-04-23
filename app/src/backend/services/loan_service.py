from datetime import datetime
from src.backend.extensions.database import db
from src.backend.models.loan import BookLoan


def create_loan(form, reader_id: int, book_id: int) -> BookLoan:
    loan = BookLoan(
        reader_id=reader_id,
        book_id=book_id,
        loan_date=datetime.now(),
        due_date=datetime.combine(form.due_date.data, datetime.now().time()),
    )

    db.session.add(loan)

    return loan


def count_delayed_books(self) -> int:
    today = datetime.now().date()

    loan_records = db.session.query(BookLoan).all()

    return sum(
        1
        for loan_record in loan_records
        if loan_record.return_date and loan_record.return_date.date() < today
    )


def count_books_due_today() -> int:
    today = datetime.now().date()

    loan_records = db.session.query(BookLoan).all()

    return sum(
        1
        for loan_record in loan_records
        if loan_record.return_date and loan_record.return_date.date() == today
    )


def has_active_loan(reader_id: int, book_id: int):
    """Verifica se o usuário já possui um empréstimo ativo para o mesmo livro."""
    return (
        db.session.query(BookLoan)
        .filter_by(reader_id=reader_id, book_id=book_id, return_date=None)
        .first()
        is not None
    )
