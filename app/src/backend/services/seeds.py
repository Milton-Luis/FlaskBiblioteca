from src.backend.extensions.database import db
from src.backend.models.models import Admin, Librarian, Role


def seed_roles():
    """Create default system roles"""

    if Role.query.first():
        return
    
    db.session.add_all([
        Admin(),
        Librarian()
    ])

    db.session.commit()
