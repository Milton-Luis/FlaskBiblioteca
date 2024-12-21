from flask_login import LoginManager

from app.backend.model.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def login_manager_app_settings(app):
    login_manager.login_view = app.config.LOGIN_VIEW
    login_manager.login_message = "Faça o login antes de acessar a página"
    login_manager.login_message_category = app.config.LOGIN_MESSAGE_CATEGORY
    login_manager.needs_refresh_message = (
        "Para garantir a segurança do seu acesso, por favor faça o login novamente"
    )
    login_manager.refresh_view = app.config.LOGIN_REFRESH_VIEW
    login_manager.needs_refresh_message_category = app.config.LOGIN_MESSAGE_CATEGORY
    login_manager.session_protection = app.config.LOGIN_SESSION_PROTECTION


# def login_manager_anonymous_settings():
#     login_manager.anonymous_user = CustomAnonymousUser


def init_app(app):
    (login_manager.init_app(app),)
    login_manager_app_settings(app)
