from datetime import datetime

from src.backend.models.reader import Reader
from src.backend.models.books import Books
from src.backend.components.components import STATUS_MAPPING
from src.backend.extensions.database import db
from src.backend.models.loan import BookLoan
from src.backend.services.book_service import borrow_book


def create_loan(form, reader: Reader, book: Books) -> BookLoan:
    if reader is None:
        raise ValueError("Leitor não emcontrado")
    
    if book is None:
        raise ValueError("Livro não emcontrado")
    
    if has_active_loan(reader.id):
        raise ValueError("Leitor já possui um empréstimo ativo.")

    loan = BookLoan(
        reader_id=reader.id,
        book_id=book.id,
        loan_date=datetime.now(),
        due_date=datetime.combine(form.due_date.data, datetime.now().time()),
    )

    db.session.add(loan)

    borrow_book(book)

    return loan

def renew_loan(loan_id: int, reader: Reader, form):
    loan=get_loan(loan_id)
    
    if loan is None:
        raise ValueError("Empréstimo não encontrado")
    
    if loan.reader_id != reader.id:
        raise ValueError(f"Este empréstimo não pertende ao {reader.fullname}")
    
    loan.return_date = datetime.now()

    new_loan = BookLoan(
        reader_id=reader.id,
        book_id=loan.book_id,
        loan_date=datetime.now(),
        due_date=datetime.combine(form.due_date.data, datetime.now().time())
    )

    db.session.add(new_loan)

    return new_loan

def get_loan(loan_id:int):
    loan = db.session.get(BookLoan, loan_id)

    return loan if loan else None

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


def has_active_loan(reader_id: int) -> bool:
    """Verifica se o usuário já possui um empréstimo ativo."""
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
