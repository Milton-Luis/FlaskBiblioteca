from ast import Is
import uuid
from datetime import datetime, timedelta
from typing import List

from flask import abort, current_app
from flask_login import UserMixin, current_user
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.extensions.database import db
from app.backend.extensions.mail import send_email


class LendingBooks(db.Model):
    __tablename__ = "lending_book"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    book_id: Mapped[int] = mapped_column(db.ForeignKey("book.id"))
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))

    users: Mapped["User"] = db.relationship(back_populates="books")
    books: Mapped["Books"] = db.relationship(back_populates="users")

    lending_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime]
    quantity_lent: Mapped[int] = mapped_column(nullable=False, default=1)

    def get_formated_date(self, date):
        return date.strftime("%d/%m/%Y")

    def check_delayed_date(self):
        self.current_date = datetime.now().date()
        delayed_dates = db.session.query(LendingBooks).all()
        for delayed_date in delayed_dates:
            return (
                True if delayed_date.return_date.date() < self.current_date else False
            )

    def count_delayed_books(self):
        self.current_date = datetime.now().date()
        books = 0
        delayed_books = db.session.query(LendingBooks).all()
        for delayed_book in delayed_books:
            if delayed_book.return_date.date() < self.current_date:
                books += 1
        return books

    def send_notification_of_return_book(self):
        # self.notification = db.session.query(LendingBooks)
        # self.notice_date = self.return_date - timedelta(days=2)

        # if self.notice_date:
        #     for lending in self.notification:
        #         send_email(
        #             lending.users.email,
        #             f"Lembrete: Devolução do livro {lending.books.get_title()}",
        #             "auth/email/reminder",
        #         )
        pass

    def count_day_return(self):
        current_date = datetime.now().date()
        delayed_books = db.session.query(LendingBooks).all()
        total_count = 0
        for delayed_book in delayed_books:
            if delayed_book.return_date.date() == current_date:
                total_count += 1
        return total_count

    def check_day_return(self):
        current_date = datetime.now().date()

        tomorrow = current_date + timedelta(days=1)

        return_days = db.session.query(LendingBooks).all()

        for return_day in return_days:
            if return_day.return_date.date() == tomorrow:
                return True
        return False


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        db.String(100), unique=True, default=str(uuid.uuid4())
    )
    firstname: Mapped[str] = mapped_column(db.String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    fullname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(
        db.String(15), nullable=False, unique=True, default="(00)90000-0000"
    )
    registered_on: Mapped[datetime] = mapped_column(
        nullable=True, default=datetime.now()
    )

    roles_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), nullable=True)
    roles: Mapped["Role"] = db.relationship(back_populates="user")

    students: Mapped[List["Students"]] = db.relationship(
        back_populates="users", cascade="all, delete-orphan"
    )

    books: Mapped[list["LendingBooks"]] = db.relationship(
        back_populates="users", cascade="all, delete-orphan"
    )

    def get_fullname(self):
        return self.fullname

    def set_fullname(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = f"{self.firstname} {self.lastname}"
        return self.fullname

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

    def get_role(self):
        return self.type.capitalize()


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

    user_id: Mapped[str] = mapped_column(db.ForeignKey("user.id"))

    users: Mapped["User"] = db.relationship(back_populates="students")

    def is_student(self):
        return "Estudante"

    def get_course(self):
        return f"{self.is_student()}: {self.grade}/{self.classroom.capitalize()}"


class Books(db.Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(60))
    author: Mapped[str] = mapped_column(db.String(60))
    isbn: Mapped[str] = mapped_column(db.String(20))
    total_of_books: Mapped[int] = mapped_column(nullable=False, default=1)
    avaiable_quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    users: Mapped[list["LendingBooks"]] = db.relationship(back_populates="books")

    def get_title(self):
        return self.title

    def get_avaiable_quantity(self):
        return self.avaiable_quantity

    def get_author(self):
        return self.author

    def get_isbn(self):
        return self.isbn

    def get_total_of_books(self):
        return self.total_of_books

    def count_total_of_books(self):
        total_books = db.session.query(func.sum(Books.total_of_books)).scalar()
        return total_books if total_books else 0

    def subtract_avaiable_quantity(self, quantity_lend: int) -> int:
        # self.avaiable_quantity = avaiable_quantity
        if self.avaiable_quantity is None:
            raise Exception("Quantidade de livros disponível não definida.")

        if quantity_lend > self.avaiable_quantity:
            raise Exception("Quantidade de livros indisponível.")

        self.avaiable_quantity -= quantity_lend
        db.session.commit()

        return self.avaiable_quantity

    def add_avaiable_quantity(self, quantity_lend: int) -> int:
        if self.avaiable_quantity is None:
            raise Exception("Quantidade de livros disponível não definida.")

        self.avaiable_quantity += quantity_lend
        db.session.commit()

        return self.avaiable_quantity

    def __repr__(self):
        return f"Livro(s): {self.title}"
