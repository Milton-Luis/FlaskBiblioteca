from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from src.backend.utils.utils import format_date
from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .books import Books
    from .reader import Reader


class BookLoan(db.Model):
    __tablename__ = "book_loans"

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(db.ForeignKey("books.id"), nullable=False)
    reader_id: Mapped[int] = mapped_column(db.ForeignKey("readers.id"), nullable=False)

    book: Mapped["Books"] = db.relationship("Books", back_populates="loan")
    reader: Mapped["Reader"] = db.relationship("Reader", back_populates="loan")

    loan_date: Mapped[datetime] = mapped_column(nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)

    def is_overdue(self) -> bool:
        """Verifica se o livro está atrasado com base na data de retorno."""
        return self.return_date and self.return_date.date() < datetime.now().date()

    def is_due_today(self) -> bool:
        """Verifica se o livro tem data de retorno para hoje."""
        return self.return_date and self.return_date.date() == datetime.now().date()

    def formatted_loan_date(self) -> str:
        """Formata a data de empréstimo para exibição."""
        return format_date(self.loan_date)
    
    def formatted_due_date(self) -> str:
        """Formata a data de retorno para exibição."""
        return format_date(self.due_date)   