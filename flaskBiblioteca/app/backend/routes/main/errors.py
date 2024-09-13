from flask import render_template

from . import main


@main.app_errorhandler(400)
def handle_csrf_error(e):
    return render_template("errors/csrf_error.html", reason=e.description), 400


@main.app_errorhandler(403)
def forbidden(e):
    return render_template(
        "errors/403.html", title="403 - Proíbido", icon="forbidden"
    ), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template(
        "errors/404.html", title="404 - Página não encontrada", icon="page_not_found"
    ), 404


@main.app_errorhandler(500)
def internal_error(e):
    return render_template("errors/500.html", title="500 - Erro no servidor"), 500
