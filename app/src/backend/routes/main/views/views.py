from flask import flash, redirect, render_template, url_for
from flask_login import current_user
from src.backend.services import book_service, loan_service

from .. import main


@main.before_app_request
def before_app_request():
    ...
    # return loan_services.send_notification_of_return_book()


@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))

    flash("Bem-vindo à Biblioteca!", "success")

    book_total = book_service.sum_total_of_books()
    monthly_loans = loan_service.count_monthly_returns()
    delayed_loans = loan_service.count_delayed_loans()
    due_today = loan_service.count_books_due_today()

    return render_template(
        "pages/index.html",
        title="Início",
        book_total=book_total,
        monthly_loans=monthly_loans,
        delayed_loans=delayed_loans,
        due_today=due_today,
    )
