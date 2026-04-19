import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.extensions.database import db

from src.backend.models.roles import RolesMixin

if TYPE_CHECKING:
    from .book_loan import BookLoan

    from .roles import Roles


class User(db.Model, UserMixin, RolesMixin):
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
    role: Mapped["Roles"] = db.relationship(back_populates="user")

    loan: Mapped[list["BookLoan"]] = db.relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def get_id(self) -> str:
        return str(self.id)

    def set_fullname(self, firstname: str, lastname: str) -> str:
        return f"{firstname} {lastname}"

    def __str__(self) -> str:
        return f"{self.fullname}"
