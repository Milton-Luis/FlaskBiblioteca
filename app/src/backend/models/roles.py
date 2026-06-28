from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .users import User


class RolesMixin:
    def has_role(self, role_name: str) -> bool:
        """
        Verifica se o usuário tem uma role específica.
        """
        if hasattr(self, "role") and self.role:
            return self.role.type.lower() == role_name.lower()
        return False


class Roles(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(db.String(11))

    user: Mapped["User"] = db.relationship(
        back_populates="role",
        uselist=False,
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_identity": "role",
        "polymorphic_on": "type",
    }

    def __str__(self) -> str:
        return self.type.capitalize()


class Admin(Roles):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=True, unique=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}


class Librarian(Roles):
    __tablename__ = "librarian"

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "librarian"}
