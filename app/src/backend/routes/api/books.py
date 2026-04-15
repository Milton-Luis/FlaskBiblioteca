from flask import jsonify, render_template, request
from flask_login import login_required
from sqlalchemy.sql import asc, or_

from src.backend.models.users import Books

from . import api


@api.route("/livros/search", methods=["GET"])
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
        books_list = [{"title": book.title, "author": book.author} for book in books]
        return jsonify(books_list)
    return render_template("partials/_books_list.html", books=books)
