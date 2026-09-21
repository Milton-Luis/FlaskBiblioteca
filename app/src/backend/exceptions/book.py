from .base import AppError


class BookNotFoundError(AppError):
    """Exception raised when a book is not found in the database."""
    def __init__(self, book: str | int) -> None:
        self.book = book
        super().__init__(f"Livro '{book}' não encontrado.")
