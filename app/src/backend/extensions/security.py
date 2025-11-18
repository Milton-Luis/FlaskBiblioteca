from flask import current_app, flash
from flask_argon2 import Argon2
from flask_cors import CORS
from itsdangerous import SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer

from src.backend.extensions.mail import send_email
from src.backend.models.models import User

argon2 = Argon2()


def generate_password(password: str) -> str:
    """Generate Password

    Args:
        * password: __type__: str

    Returns:
        str: create a hashed password
    """
    return argon2.generate_password_hash(password)


def check_password(password_hash: str, password: str) -> bool:
    """check Password

    Args:
        * password_hash (str): hash password argument
        * password (str): password created

    Returns:
        bool: compares hashed password with the password passed at login
    """
    return argon2.check_password_hash(password_hash, password)


def generate_confirmation_token(email: str) -> str:
    """Generate a confirmation token for the given email.

    The token is generated using a secret key and a salt, and is valid for activating a user account.
    Args:
        * email (str): user email

    Returns:
        str: creates a confirmation token
    """
    serial = Serializer(current_app.config("TOKEN_SECRET_KEY"))
    return serial.dumps(email, salt=current_app.config["SECURITY_PASSWORD_ACTIVATE"])


def validate_token(token: str, expiration=3600) -> str:
    """Validate Token

    Args:
        * token (str): token sended
        * expiration: time to token expires. Default 3600 seconds.

    Raises:
        False: if the time expired or used another token

    Returns:
       bool: the email adress associated with the token
    """
    serial = Serializer(current_app.config["TOKEN_SECRET_KEY"])
    try:
        email = serial.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_ACTIVATE"],
            max_age=expiration,
        )
    except SignatureExpired:
        return None
    return email


def access_confirmation(user):
    token = generate_confirmation_token(user.email)
    try:
        send_email(
            user.email,
            "Confirme seu email",
            "auth/email/confirm",
            user=user,
            token=token,
        )
    except Exception as e:
        flash(f"Erro ao enviar o email de confirmação {e}", "danger")
    else:
        flash("Um email de confirmação foi enviado a você", "info")


def init_app(app):
    return argon2.init_app(app), CORS(app)
