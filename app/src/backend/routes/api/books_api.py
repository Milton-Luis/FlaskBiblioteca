from flask import jsonify, render_template, request
from flask_login import login_required
from sqlalchemy.sql import asc, or_
from src.backend.models.books import Books

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

    return render_template("partials/_books_list.html", books=books)
