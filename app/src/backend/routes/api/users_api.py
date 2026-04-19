from flask import jsonify, request
from flask_login import login_required
from sqlalchemy.sql import asc

from src.backend.extensions.database import db
from src.backend.models.users import User
from src.backend.models.books import Books

from . import api


@api.route("/emprestimos/novo/<slug>/search", methods=["GET"])
@login_required
def search_borrower(slug):
    search = request.args.get("q", "")

    db.session.query(Books).filter_by(slug=slug).first()

    users = User.query.filter(User.fullname.ilike(f"%{search}%")).order_by(
        asc(User.firstname)
    )
    name_list = []
    for user in users.all():
        name_list.append({"id": user.id,"fullname": user.fullname})
    return jsonify(name_list)
