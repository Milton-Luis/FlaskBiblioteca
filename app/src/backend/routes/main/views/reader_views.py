from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from src.backend.extensions.database import db
from src.backend.routes.main import main
from src.backend.routes.main.forms import ReaderForm
from src.backend.services import reader_service


@main.route("/leitor/novo", methods=["POST", "GET"])
@login_required
def new_reader():
    form = ReaderForm()

    if form.validate_on_submit():
        try:
            reader_service.create_reader(form)
            db.session.commit()

            flash("Novo leitor adicionado!!", "success")
        except Exception:
            db.session.rollback()
            flash("Erro ao adicionar informações", "danger")
        return redirect(url_for("main.index"))

    return render_template(
        "pages/new_reader.html", form=form, title="Adicionar novo Leitor"
    )
