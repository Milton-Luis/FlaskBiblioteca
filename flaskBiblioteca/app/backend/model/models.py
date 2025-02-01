import uuid
from datetime import datetime
from typing import List

from app.backend.extensions.database import db
from flask import abort, current_app
from flask_login import UserMixin, current_user
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class LendingBooks(db.Model):
    __tablename__ = "lending_book"
    book_id: Mapped[int] = mapped_column(
        db.ForeignKey("book.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), primary_key=True, nullable=False
    )

    users: Mapped["User"] = db.relationship(back_populates="books")
    books: Mapped["Books"] = db.relationship(back_populates="users")

    lending_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now()
    )
    return_date: Mapped[datetime]
    quantity_lent: Mapped[int] = mapped_column(nullable=False, default=1)

    def get_formated_date(self, date: datetime):
        self.formated_date = date.strftime("%d/%m/%Y")
        [self.lending_date, self.return_date] = self.formated_date
        return self.formated_date


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

    roles_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), nullable=True)
    roles: Mapped["Role"] = db.relationship(back_populates="user")

    student: Mapped[List["Students"]] = db.relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    books: Mapped[list["LendingBooks"]] = db.relationship(
        back_populates="users", cascade="all, delete-orphan"
    )

    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self) -> str:
        return f"User {self.email}"


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    rolename: Mapped[str] = mapped_column(db.String(2), nullable=False, default="LB")
    password: Mapped[str] = mapped_column(db.String(256), nullable=False, unique=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    type: Mapped[str]

    user: Mapped["User"] = db.relationship(
        back_populates="roles",
        uselist=False,
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_identity": "role",
        "polymorphic_on": "type",
    }


class Admin(Role):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)
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

    id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "librarian"}


class Students(db.Model):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom: Mapped[str] = mapped_column(db.String(15))
    grade: Mapped[str] = mapped_column(db.String(2))

    user: Mapped["User"] = db.relationship(back_populates="student", uselist=False)

    user_id: Mapped[str] = mapped_column(db.ForeignKey("user.id"))


class Books(db.Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(60))
    author: Mapped[str] = mapped_column(db.String(60))
    isbn: Mapped[str] = mapped_column(db.String(20))
    quantity_of_books: Mapped[int] = mapped_column(nullable=False, default=1)

    users: Mapped[list["LendingBooks"]] = db.relationship(back_populates="books")

    def get_total_books(self):
        total_books = db.session.query(func.sum(Books.quantity_of_books)).scalar()
        return total_books if total_books else 0

    def get_title(self):
        return self.title

    def get_delayed_books(self):
        delayed_books = db.session.query(func.sum(LendingBooks.return_date)).scalar()
        return delayed_books if delayed_books else 0
