from flask import jsonify, request, session
from flask_login import login_required
from sqlalchemy.sql import asc

from src.backend.extensions.database import db
from src.backend.models.reader import Reader

from . import api


@api.route("/emprestimos/novo/<slug>/search", methods=["GET"])
@login_required
def search_reader(slug):
    search = request.args.get("q", "")

    if not search:
        return jsonify([])

    readers = (
        db.session.query(Reader)
        .filter(Reader.fullname.ilike(f"%{search}%"))
        .order_by(asc(Reader.firstname)).all()
    )

    return jsonify([
        {"id":reader.id, "fullname": reader.fullname} for reader in readers
    ])

@api.route("/emprestimos/selecionar-usuario", methods=["POST"])
@login_required
def select_reader():
    data = request.get_json()

    session["reader_id"] = data["reader_id"]

    return jsonify({"ok": True})