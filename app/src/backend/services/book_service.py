from sqlalchemy import func
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.utils.utils import slugfy


def create_book(form):
    """Cria um novo livro com base nos dados do formulário e salva no banco de dados."""
    book = Books()

    form.populate_obj(book)
    book.slug = slugfy(book.title)
    book.available_quantity = book.total_of_books

    db.session.add(book)

    return book


def get_book(book_id: int):
    book = db.session.get(Books, book_id)
    if not book:
        raise ValueError("Livro não encontrado")
    return book


def borrow_book(book_id: int) -> int:
    book = get_book(book_id)

    if not book:
        raise ValueError("Livro não encontrado")

    book.decrease_stock(1)
    return book


def return_book(book_id: int) -> int:
    book = get_book(book_id)

    if not book:
        raise ValueError("Livro não encontrado")

    book.increase_stock(1)
    return book


def sum_total_of_books():
    total_books = db.session.query(func.count(func.distinct(Books.title))).scalar()
    return total_books or 0
