from datetime import datetime

from src.backend.extensions.database import db
from src.backend.models.models import LendingBooks


def get_formated_date(date: datetime) -> str:
    return date.strftime("%d/%m/%Y")


def count_delayed_books() -> int:
    current_date = datetime.now().date()
    delayed_books_count = 0
    lending_records = db.session.query(LendingBooks).all()
    for lending_record in lending_records:
        if lending_record.return_date.date() < current_date:
            delayed_books_count += 1
    return delayed_books_count


def count_monthly_returns() -> int: ...


# def send_notification_of_return_book(user_id: int) -> None:
#     notifications = db.session.query(LendingBooks).filter_by(
#         user_id=user_id
#     ).all()
#     return_date = datetime.now().date() + timedelta(days=1)
#     notice_date = return_date - timedelta(days=2)

#     if notice_date:
#         for lending in notifications:
#             send_email(
#                 lending.users.email,
#                 f"Lembrete: Devolução do livro {lending.books.title}",
#                 "auth/email/reminder",
#             )


def count_books_due_today() -> int:
    today = datetime.now().date()
    books_due_today_count = 0

    lending_records = db.session.query(LendingBooks).all()
    for lending_record in lending_records:
        if lending_record.return_date.date() == today:
            books_due_today_count += 1
    return books_due_today_count
