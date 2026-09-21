from sqlalchemy import func, asc
from src.backend.extensions.database import db
from src.backend.models.books import Books
from src.backend.utils.utils import slugfy
from src.backend.exceptions.book import BookNotFoundError


def create_book(form):
    """Cria um novo livro com base nos dados do formulário e salva no banco de dados."""
    book = Books()

    form.populate_obj(book)
    book.slug = slugfy(book.title)
    book.available_quantity = book.total_of_books

    db.session.add(book)

    return book


def get_all_books():
    books = db.select(Books).order_by(asc(Books.title))
    return books


def get_book_by_slug(slug: str) -> Books:
    book = db.session.query(Books).filter_by(slug=slug).first()
    if book is None:
        raise BookNotFoundError(slug)
    return book


def get_book_by_id(book_id: int) -> Books:
    book = db.session.get(Books, book_id)
    if book is None:
        raise BookNotFoundError(book_id)
    return book


def borrow_book(book: int) -> int:
    # book = get_book_by_id(book_id)

    if not book:
        raise ValueError("Livro não encontrado")

    book.decrease_stock(1)
    return book


def return_book(book_id: int) -> int:
    book = get_book_by_id(book_id)

    if not book:
        raise ValueError("Livro não encontrado")

    book.increase_stock(1)
    return book


def sum_total_of_books():
    total_books = db.session.query(func.count(func.distinct(Books.title))).scalar()
    return total_books or 0
