from datetime import datetime, timedelta
from app.backend.extensions.database import db
from app.backend.model.models import LendingBooks


def get_formated_date(date: datetime) -> str:
    return date.strftime("%d/%m/%Y")


def check_delayed_date() -> bool:
    current_date = datetime.now().date()
    delayed_dates = db.session.query(LendingBooks).all()
    for delayed_date in delayed_dates:
        return True if delayed_date.return_date.date() < current_date else False


def count_delayed_books() -> int:
    current_date = datetime.now().date()
    books = 0
    delayed_books = db.session.query(LendingBooks).all()
    for delayed_book in delayed_books:
        if delayed_book.return_date.date() < current_date:
            books += 1
    return books


# def send_notification_of_return_book(id:int) -> None:
# .notification = db.session.query(LendingBooks).filter_by(
#     user_id=idreturn_date=.return_date
# ).all()
# .return_date = datetime.now().date() + timedelta(days=1)
# .notice_date = .return_date - timedelta(days=2)

# if .notice_date:
#     for lending in .notification:
#         send_email(
#             lending.users.email,
#             f"Lembrete: Devolução do livro {lending.books.title}",
#             "auth/email/reminder",
#         )


def count_day_return() -> int:
    current_date = datetime.now().date()
    delayed_books = db.session.query(LendingBooks).all()
    total_count = 0
    for delayed_book in delayed_books:
        if delayed_book.return_date.date() == current_date:
            total_count += 1
    return total_count


def check_day_return() -> bool:
    current_date = datetime.now().date()
    tomorrow = current_date + timedelta(days=1)
    return_days = db.session.query(LendingBooks).all()

    for return_day in return_days:
        if return_day.return_date.date() == tomorrow:
            return True
    return False
