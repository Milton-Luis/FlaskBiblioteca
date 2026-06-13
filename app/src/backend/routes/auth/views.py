from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src.backend.extensions.database import db
from src.backend.security.tokens import validate_token
from src.backend.models.users import User
from src.backend.utils.utils import is_safe_url
from src.backend.services.auth_service import redirect_user_dashboard

from . import auth
from .forms import LoginForm


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.is_confirmed
        and request.blueprint != "auth"
        and request.endpoint not in ("static", "unconfirmed")
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if current_user.is_authenticated and current_user.is_confirmed:
        return redirect_user_dashboard(current_user)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            next_page = request.args.get("next")

            if next_page and is_safe_url(next_page, request.host):
                return redirect(next_page)
            
            endpoint = redirect_user_dashboard(user)
            return redirect(url_for(endpoint))

        flash("Usuário ou senha invalidos", "danger")
    return render_template("pages/auth/login.html", form=form, title="Login")


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
        flash("Seu acesso foi confirmado, bem vindo.", "info")
    return redirect(url_for("auth.login"))


@auth.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect("main.index")
    return render_template("pages/auth/unconfirmed.html")


@auth.route("/perfil", methods=["POST", "GET"])
def profile():
    return render_template("pages/auth/profile.html", title="Perfil")
