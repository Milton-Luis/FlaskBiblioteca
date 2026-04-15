import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .lending import LendingBooks


class RoleMixin:
    def has_role(self, role_name: str) -> bool:
        """
        Verifica se o usuário tem uma role específica.
        """
        if hasattr(self, "role") and self.role:
            return self.role.type.lower() == role_name.lower()
        return False


class User(db.Model, UserMixin, RoleMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        db.String(100), unique=True, default=str(uuid.uuid4())
    )
    firstname: Mapped[str] = mapped_column(db.String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    fullname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(256), nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    registered_on: Mapped[datetime] = mapped_column(
        nullable=True, default=datetime.now()
    )

    role_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = db.relationship(back_populates="user")

    books: Mapped[list["LendingBooks"]] = db.relationship(
        back_populates="users", cascade="all, delete-orphan"
    )

    def get_id(self) -> str:
        return str(self.id)

    def set_fullname(self, firstname: str, lastname: str) -> str:
        return f"{firstname} {lastname}"

    def __str__(self) -> str:
        return f"{self.fullname} - {self.email}"


class Role(db.Model):
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


class Admin(Role):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=True, unique=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}


class Librarian(Role):
    __tablename__ = "librarian"

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "librarian"}
