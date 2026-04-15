import uuid
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.extensions.database import db


class RoleMixin:
    def has_role(self, role_name: str) -> bool:
        """
        Verifica se o usuário tem uma role específica.
        """
        if hasattr(self, "role") and self.role:
            return self.role.type.lower() == role_name.lower()
        return False


class LendingBooks(db.Model):
    __tablename__ = "lending_book"

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(db.ForeignKey("books.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)

    users: Mapped["User"] = db.relationship(back_populates="books")
    books: Mapped["Books"] = db.relationship(back_populates="users")

    lending_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)
    quantity_lent: Mapped[int] = mapped_column(nullable=False, default=1)


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


class Books(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(60))
    slug: Mapped[str] = mapped_column(db.String(60))
    author: Mapped[str] = mapped_column(db.String(60))
    isbn: Mapped[str] = mapped_column(db.String(20))
    total_of_books: Mapped[int] = mapped_column(nullable=False, default=1)
    available_quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    users: Mapped[list["LendingBooks"]] = db.relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Livro(s): {self.title} - Autor: {self.author} - Quantidade: {self.total_of_books} - Disponível: {self.available_quantity}"

    def __str__(self):
        return self.title
