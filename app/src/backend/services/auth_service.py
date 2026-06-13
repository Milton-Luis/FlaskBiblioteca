from src.backend.security.tokens import generate_confirmation_token
from src.backend.extensions.mail import send_email
from src.backend.models.users import User
from dynaconf import settings


def access_confirmation(user):
    token = generate_confirmation_token(user.email)
    
    send_email(
        user.email,
        "Confirme seu email",
        "pages/email/confirm",
        user=user,
        token=token,
    )

def redirect_user_dashboard(user: User) -> str:
    if user.has_role(settings.ROLES["admin"]):
        return settings.URL_FOR["admin"]
    else:
        return settings.URL_FOR["main"]
