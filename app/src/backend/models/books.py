from typing import TYPE_CHECKING

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

    def __repr__(self) -> str:
        return f"Livro(s): {self.title} - Autor: {self.author} - Quantidade: {self.total_of_books} - Disponível: {self.available_quantity}"

    def __str__(self):
        return self.title