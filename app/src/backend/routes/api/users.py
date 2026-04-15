from flask import jsonify, request
from flask_login import login_required
from sqlalchemy.sql import asc

from src.backend.extensions.database import db
from src.backend.models.users import Books, User

from . import api


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
