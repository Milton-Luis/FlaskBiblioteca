from app.backend.extensions.database import db
from app.backend.model.models import Books
from sqlalchemy import func


def subtract_available_quantity(book_id: int, quantity_to_lend: int) -> int:
    book = db.session.query(Books).filter_by(id=book_id).first()
    if quantity_to_lend > book.available_quantity:
        raise ValueError("Quantidade de livros indisponível")
    book.available_quantity -= quantity_to_lend
    return book.available_quantity


def add_available_quantity(book_id: int, quantity_to_lend: int) -> int:
    book = db.session.query(Books).filter_by(id=book_id).first()
    if quantity_to_lend > book.available_quantity:
        raise ValueError("mais livros disponíveis do que o total")
    book.available_quantity += quantity_to_lend
    return book.available_quantity


def sum_total_of_books():
    total_books = db.session.query(func.sum(Books.total_of_books)).scalar()
    return total_books or 0

