import re
import unicodedata
from datetime import datetime, timedelta
from urllib.parse import urlparse

from dynaconf import settings
from flask import Response, redirect, request, url_for

from src.backend.models.users import User


def slugfy(text: str) -> str:
    # remove os acentos
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mm")

    # converte para minúsculas
    text = text.lower().strip()

    # remove caracteres especiais
    text = re.sub(r"[^a-z0-9\s-]", "", text)

    # troca espaços por hífens
    text = re.sub(r"\s+", "-", text)

    # remove multiplos hífens
    text = re.sub(r"-+", "-", text)

    return text


def redirect_user_dashboard(user: User) -> Response:
    if user.has_role(settings.ROLES[0]):
        return redirect(url_for(settings.URL_FOR[0]))
    else:
        return redirect(url_for(settings.URL_FOR[1]))


def is_safe_url(url) -> bool:
    if not url:
        return False
    try:
        parsed_url = urlparse(url)
        return (
            parsed_url.scheme == "" and parsed_url.netloc == ""
        ) or parsed_url.netloc == request.host
    except Exception:
        return False


def renew_loan(loan):
    if loan.return_date:
        loan.return_date += timedelta(days=7)
    else:
        loan.return_date = datetime.now() + timedelta(days=7)
