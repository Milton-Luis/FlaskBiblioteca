from src.backend.security.tokens import generate_confirmation_token
from src.backend.extensions.mail import send_email


def access_confirmation(user):
    token = generate_confirmation_token(user.email)
    
    send_email(
        user.email,
        "Confirme seu email",
        "pages/email/confirm",
        user=user,
        token=token,
    )

