import re
from unicodedata import normalize


def slugify(title: str) -> str:
    slug = title.lower()
    slug = normalize("NFKD", slug)
    slug = slug.encode("ascii", "ignore").decode("utf-8")
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)

    return slug
