import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from src.backend.extensions.database import db
from src.backend.extensions.security import argon2
from src.backend.models.roles import RolesMixin

if TYPE_CHECKING:
    from .roles import Roles


class User(db.Model, UserMixin, RolesMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        db.String(100), unique=True, default=lambda:str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)

    is_confirmed: Mapped[bool] = mapped_column(default=False)
    registered_on: Mapped[datetime] = mapped_column(
        nullable=True, default=datetime.now()
    )

    role_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), nullable=True)
    role: Mapped["Roles"] = db.relationship(back_populates="user")

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only")


    @password.setter
    def password(self, password: str) -> None:
        """Generate Password

        Args:
            * password: __type__: str

        Returns:
            str: create a hashed password
        """
        self.password_hash = argon2.generate_hash_password(password)

    def check_password(self, password: str) -> bool:
        """check Password

        Args:
            * password_hash (str): hash password argument
            * password (str): password created

        Returns:
            bool: compares hashed password with the password passed at login
        """
        if not password:
            return False
        return argon2.check_hash_password(self.password_hash, password)
