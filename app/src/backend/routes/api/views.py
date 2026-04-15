from flask import jsonify, request, render_template
from flask_login import login_required
from sqlalchemy.sql import asc, or_

from src.backend.extensions.database import db
from src.backend.models.models import Books, User

from . import api


@api.get("/livros/search")
@login_required
def search_books():
    search = request.args.get("q", "")
    books = (
        Books.query.filter(
            or_(
                Books.title.like(f"%{search}%"),
                Books.author.startswith(f"{search}"),
            )
        )
        .order_by(asc(Books.title))
        .all()
    )

    if (
        request.args.get("format") == "json"
        or request.accept_mimetypes["application/json"]
    ):
        books_list = [
            {"title": book.title, "author": book.author} for book in books
        ]
        return jsonify(books_list)
    return render_template("partials/_books_list.html", books=books)


@api.route("/emprestimos/novo/<slug>/search", methods=["GET"])
@login_required
def request_search_borrower(slug):
    db.session.query(Books).filter(Books.slug == slug).first()
    search = request.args.get("q", "")
    get_user = User.query.filter(User.fullname.ilike(f"%{search}%")).order_by(
        asc(User.firstname)
    )
    name_list = []
    for user in get_user.all():
        name_list.append({"fullname": user.fullname})
    return jsonify(name_list)
