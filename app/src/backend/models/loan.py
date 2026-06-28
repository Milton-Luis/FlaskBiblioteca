from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import and_, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from src.backend.components.components import STATUS_MAPPING
from src.backend.extensions.database import db
from src.backend.utils.utils import format_date, today_date

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

    @hybrid_property
    def status(self) -> str:
        today = today_date()

        if self.return_date is not None:
            return STATUS_MAPPING["returned"]
        elif self.due_date.date() < today:
            return STATUS_MAPPING["overdue"]
        elif self.due_date.date() == today:
            return STATUS_MAPPING["due_today"]
        else:
            return STATUS_MAPPING["on_time"]

    @status.expression
    def status(cls):
        today = func.current_date()

        return db.case(
            (cls.return_date.is_not(None), STATUS_MAPPING["returned"]),  # noqa E711
            (
                and_(cls.return_date.is_(None), func.date(cls.due_date) == today),
                STATUS_MAPPING["due_today"],
            ),
            (
                and_(cls.return_date.is_(None), func.date(cls.due_date) < today),
                STATUS_MAPPING["overdue"],
            ),
            else_=STATUS_MAPPING["on_time"],
        )

    def is_overdue(self) -> bool:
        """Verifica se o livro está atrasado com base na data de retorno."""
        today = today_date()
        return (self.return_date is None) and (self.due_date.date() < today)

    def is_due_today(self) -> bool:
        """Verifica se o livro tem data de retorno para hoje."""
        today = today_date()
        return (self.return_date is None) and (self.due_date.date() == today)

    def formatted_loan_date(self) -> str:
        """Formata a data de empréstimo para exibição."""
        return format_date(self.loan_date)

    def formatted_due_date(self) -> str:
        """Formata a data de retorno para exibição."""
        return format_date(self.due_date)
