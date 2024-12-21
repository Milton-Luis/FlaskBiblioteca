from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.backend.extensions.database import db
from app.backend.extensions.security import check_password, validate_token
from app.backend.model.models import User
from app.backend.utils.operations import Services

from . import auth
from .forms import LoginForm


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if current_user.is_authenticated and current_user.roles.is_confirmed:
        return redirect(url_for("main.index"))

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        # user = Services.get_first_record(User, email=form.email.data)

        if user and check_password(user.roles.password, form.password.data):
            login_user(user)

            if current_user.roles.type == "admin":
                return redirect(url_for("admin.index"))

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)
            return redirect(url_for("main.index"))
        flash("Usuário ou senha invalidos", "danger")
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Você foi deslogado", "warning")
    return redirect(url_for("main.index"))


@auth.route("/confirm/<token>")
def confirm_email(token):
    email = validate_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    user = Services.get_first_record(User, email=email)

    if user.roles.is_confirmed:
        return redirect(url_for("main.index"))

    if user.email != email:
        flash("O link de confirmação é invalido ou expirou.", "danger")
    else:
        user.roles.is_confirmed = True
        user.registered_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("Seu acesso foi confirmado, bem vindo.", "success")
    return redirect(url_for("auth.login"))


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.roles.is_confirmed
        and request.blueprint != "auth"
        and request.endpoint not in ("static", "unconfirmed")
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.roles.is_confirmed:
        return redirect("main.index")
    return render_template("auth/unconfirmed.html")
