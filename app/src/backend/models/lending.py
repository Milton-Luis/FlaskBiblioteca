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

    quantity_lent: Mapped[int] = mapped_column(nullable=False)

    def get_formated_date(self, date: datetime) -> str:
        return date.strftime("%d/%m/%Y")

    def count_delayed_books(self) -> int:
        current_date = datetime.now().date()
        delayed_books_count = 0
        lending_records = LendingBooks.query.all()
        for lending_record in lending_records:
            if lending_record.return_date.date() < current_date:
                delayed_books_count += 1
        return delayed_books_count

    def count_books_due_today(self) -> int:
        today = datetime.now().date()
        books_due_today_count = 0

        lending_records = LendingBooks.query.all()
        for lending_record in lending_records:
            if lending_record.return_date.date() == today:
                books_due_today_count += 1
        return books_due_today_count

    def has_active_loan(self,user_id, book_id):
        return db.session.query(
            db.exists().where(
                LendingBooks.book_id == book_id,
                LendingBooks.user_id == user_id,
                LendingBooks.return_date.is_(None),
            )
        ).scalar()
