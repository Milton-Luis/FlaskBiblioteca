import re
import unicodedata
from datetime import datetime, timedelta
from urllib.parse import urlparse


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


def is_safe_url(url: str, host:str) -> bool:
    if not url:
        return False
    try:
        parsed_url = urlparse(url)
        return (
            parsed_url.scheme == "" and parsed_url.netloc == ""
        ) or parsed_url.netloc == host
    except Exception:
        return False


def renew_loan(loan):
    if loan.return_date:
        loan.return_date += timedelta(days=7)
    else:
        loan.return_date = datetime.now() + timedelta(days=7)


def format_date(date_value: str) -> str:
    if isinstance(date_value, datetime):
        return date_value.strftime("%d/%m/%Y")

    try:
        parsed_date = datetime.fromisoformat(date_value)
        return parsed_date.strftime("%d/%m/%Y")
    except Exception:
        return "N/A"

def today_date() -> str:
    return datetime.now().date()