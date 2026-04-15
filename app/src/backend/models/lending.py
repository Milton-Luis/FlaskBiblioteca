from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .books import Books
    from .users import User


class LendingBooks(db.Model):
    __tablename__ = "lending_book"

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(db.ForeignKey("books.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)

    users: Mapped["User"] = db.relationship(back_populates="books")
    books: Mapped["Books"] = db.relationship(back_populates="users")

    lending_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)
    quantity_lent: Mapped[int] = mapped_column(nullable=False, default=1)
