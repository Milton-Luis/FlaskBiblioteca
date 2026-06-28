from datetime import datetime

from app import db


class LoanHistory(db.Model):
    __tablename__ = "loan_history"

    id = db.Column(db.Integer, primary_key=True)

    loan_id = db.Column(
        db.Integer,
        db.ForeignKey("book_loan.id"),
        nullable=False
    )

    status = db.Column(db.String(20), nullable=False)

    changed_at = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    # relacionamento (opcional, mas recomendado)
    loan = db.relationship("BookLoan", backref="history")