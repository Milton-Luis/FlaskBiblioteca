from dynaconf import settings
from itsdangerous import SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer


def generate_confirmation_token(email: str) -> str:
    """Generate a confirmation token for the given email.

    The token is generated using a secret key and a salt, and is valid for activating a user account.
    Args:
        * email (str): user email

    Returns:
        str: creates a confirmation token
    """
    serial = Serializer(settings.TOKEN_SECRET_KEY)
    return serial.dumps(email, salt=settings.SECURITY_PASSWORD_ACTIVATE)


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
    serial = Serializer(settings.TOKEN_SECRET_KEY)
    try:
        email = serial.loads(
            token,
            salt=settings.SECURITY_PASSWORD_ACTIVATE,
            max_age=expiration,
        )
    except SignatureExpired:
        return None
    return email
