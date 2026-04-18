from src.backend.extensions.database import db
from src.backend.models.roles import Admin, Librarian, Roles


def seed_roles():
    """Create default system roles"""

    if Roles.query.first():
        return

    db.session.add_all([Admin(), Librarian()])

    db.session.commit()
