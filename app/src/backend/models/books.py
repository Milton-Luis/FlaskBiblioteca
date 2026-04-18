from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .lending import LendingBooks


class Books(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(60))
    slug: Mapped[str] = mapped_column(db.String(60))
    author: Mapped[str] = mapped_column(db.String(60))
    isbn: Mapped[str] = mapped_column(db.String(20))
    total_of_books: Mapped[int] = mapped_column(nullable=False, default=1)
    available_quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    users: Mapped[list["LendingBooks"]] = db.relationship(back_populates="books")

    def add_available_quantity(book_id: int, quantity_to_lend: int) -> int:
        book = db.session.query(Books).filter_by(id=book_id).first()
        if quantity_to_lend > book.available_quantity:
            raise ValueError("mais livros disponíveis do que o total")
        book.available_quantity += quantity_to_lend
        return book.available_quantity

    def subtract_available_quantity(book_id: int, quantity_to_lend: int) -> int:
        book = db.session.query(Books).filter_by(id=book_id).first()
        if quantity_to_lend > book.available_quantity:
            raise ValueError("Quantidade de livros indisponível")
        book.available_quantity -= quantity_to_lend
        return book.available_quantity

    def sum_total_of_books():
        total_books = db.session.query(func.sum(Books.total_of_books)).scalar()
        return total_books or 0

    def __repr__(self) -> str:
        return f"Livro(s): {self.title} - Autor: {self.author} - Quantidade: {self.total_of_books} - Disponível: {self.available_quantity}"

    def __str__(self):
        return self.title
