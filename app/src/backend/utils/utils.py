import re
import unicodedata
from urllib.parse import urlparse

from dynaconf import settings
from flask import Response, redirect, request, url_for

from src.backend.models.models import User


def slugfy(text: str) -> str:
    # remove os acentos
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mm")

    # converte para minúsculas
    text = text.lower().strip()

    # remove caracteres especiais
    text = re.sub(r"[a-z0-9\s-]", "", text)

    # troca espaços por hífens
    text = re.sub(r"\s+", "-", text)

    # remove multiplos hífens
    text = re.sub(r"-+", "-", text)

    return text


def redirect_user_dashboard(user: User) -> Response:
    role = user.role.type

    if role == settings.ROLES.ADMIN:
        return redirect(url_for("admin.index"))
    else:
        return redirect(url_for("main.index"))


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
