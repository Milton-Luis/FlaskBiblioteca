import uuid
from datetime import datetime
from typing import List

from flask import abort, current_app
from flask_login import UserMixin, current_user
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.extensions.database import db


class LoanBooks(db.Model):
    __tablename__ = "loanbooks"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(db.ForeignKey("book.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)

    loan_date: Mapped[datetime]
    return_date: Mapped[datetime]
    quantityBooks: Mapped[int] = mapped_column(nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        db.String(100), unique=True, default=str(uuid.uuid4())
    )
    firstname: Mapped[str] = mapped_column(db.String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(
        db.String(15), nullable=False, unique=True, default="(00)90000-0000"
    )
    registered_on: Mapped[datetime] = mapped_column(
        nullable=True, default=datetime.now()
    )

    roles: Mapped[List["Role"]] = db.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    student: Mapped[List["Students"]] = db.relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    books: Mapped[list["Book"]] = db.relationship(
        secondary="loanbooks", back_populates="users"
    )

    def __str__(self) -> str:
        return f"User {self.email}"


class Role(db.Model):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    rolename: Mapped[str] = mapped_column(db.String(2), nullable=False, default="LB")
    password: Mapped[str] = mapped_column(db.String(256), nullable=False, unique=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    type: Mapped[str]

    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    user: Mapped["User"] = db.relationship(back_populates="roles")

    __mapper_args__ = {
        "polymorphic_identity": "role",
        "polymorphic_on": "type",
    }


class Admin(Role):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(db.ForeignKey("role.id"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False, unique=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}

    def check_admin_permission(model):
        admin_access = current_app.config["FLASK_ADMIN_ACCESS"]
        if (model in [Librarian, User, Students]) and (
            current_user.roles.type != admin_access
        ):
            abort(403)
        return True


class Librarian(Role):
    __tablename__ = "librarian"

    id: Mapped[int] = mapped_column(db.ForeignKey("role.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "librarian"}


class Students(db.Model):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom: Mapped[str] = mapped_column(db.String(15))
    grade: Mapped[str] = mapped_column(db.String(2))

    user: Mapped["User"] = db.relationship(back_populates="student", uselist=False)

    user_id: Mapped[str] = mapped_column(db.ForeignKey("user.id"))


class Book(db.Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(60))
    author: Mapped[str] = mapped_column(db.String(60))
    isbn: Mapped[str] = mapped_column(db.String(20))

    users: Mapped[list["User"]] = db.relationship(
        secondary="loanbooks", back_populates="books"
    )
