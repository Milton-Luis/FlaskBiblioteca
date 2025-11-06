from flask import jsonify, request
from flask_login import login_required
from sqlalchemy.sql import asc, or_

from app.backend.extensions.database import db
from app.backend.model.models import Books, User

from . import api


@api.route("/livros/search", methods=["GET"])
@login_required
def search_books():
    search = request.args.get("q", "")
    books_query = (
        db.session.query(Books)
        .filter(
            or_(
                Books.title.like(f"%{search}%"),
                Books.author.startswith(f"{search}"),
            )
        )
        .order_by(asc(Books.title))
    )
    books_list = [
        {"title": book.title, "author": book.author} for book in books_query.all()
    ]
    return jsonify(books_list)

@api.route("/emprestimos/novo/<title>/search", methods=["GET"])
@login_required
def request_search_borrower(title):
    db.session.query(Books).filter(Books.title == title).first()
    search = request.args.get("q", "")
    get_user = (
        db.session.query(User)
        .filter(User.fullname.ilike(f"%{search}%"))
        .order_by(asc(User.firstname))
    )
    name_list = []
    for user in get_user.all():
        info = []  # Inicialize a info aqui para cada usuário
        if user.roles_id is None:
            for student in user.students:
                info.append({"info": student.get_course()})
        else:
            info.append({"info": user.roles.get_role()})

        name_list.append({"fullname": user.fullname, "info": info})
    return jsonify(name_list)