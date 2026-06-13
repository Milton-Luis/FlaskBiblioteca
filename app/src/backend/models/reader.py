from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

from src.backend.extensions.database import db

if TYPE_CHECKING:
    from .loan import BookLoan


class Reader(db.Model):
    __tablename__ = "readers"
    id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str] = mapped_column(db.String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)

    loan: Mapped[list["BookLoan"]] = db.relationship(
        back_populates="reader", cascade="all, delete-orphan"
    )

    @hybrid_property
    def fullname(self):
        return f"{self.firstname.title()} {self.lastname.title()}"
    
    @fullname.expression
    def fullname(cls):
        return func.concat(cls.firstname, " ", cls.lastname)


    def __str__(self):
        return self.fullname