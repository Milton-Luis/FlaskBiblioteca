from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src.backend.extensions.database import db
from src.backend.extensions.security import check_password, validate_token
from src.backend.models.models import User
from src.backend.utils.utils import is_safe_url, redirect_user_dashboard

from . import auth
from .forms import LoginForm


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if current_user.is_authenticated and current_user.is_confirmed:
        return redirect_user_dashboard(current_user)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password(user.password, form.password.data):
            login_user(user)

            next_page = request.args.get("next")

            if next_page and is_safe_url(next_page):
                return redirect(next_page)

            return redirect_user_dashboard(user)

        flash("Usuário ou senha invalidos", "danger")
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi deslogado", "warning")
    return redirect(url_for("main.index"))


@auth.route("/confirm")
def confirm_email():
    token = request.args.get("token")
    email = validate_token(token)
    user = User.query.filter_by(email=email).first_or_404()

    if user.is_confirmed:
        return redirect(url_for("main.index"))

    if user.email != email:
        flash("O link de confirmação é invalido ou expirou.", "danger")
    else:
        user.is_confirmed = True
        user.registered_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("Seu acesso foi confirmado, bem vindo.", "success")
    return redirect(url_for("auth.login"))


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.is_confirmed
        and request.blueprint != "auth"
        and request.endpoint not in ("static", "unconfirmed")
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect("main.index")
    return render_template("auth/unconfirmed.html")
