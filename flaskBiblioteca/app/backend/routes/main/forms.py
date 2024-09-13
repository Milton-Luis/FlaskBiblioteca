from datetime import datetime

from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange


class AddBookForm(FlaskForm):
    search = StringField(
        None,
        validators=[DataRequired()],
        render_kw={
            "placeholder": "digite o título do livro ou nome do autor",
            "class": "form-control",
        },
        id="searchBook",
    )
    title = StringField(
        "Título",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o título do livro"},
    )
    author = StringField(
        "Autor",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o autor do livro"},
    )
    isbnCode = StringField(
        "ISBN",
        render_kw={"placeholder": "Digite o ISBN do livro"},
    )
    quantityBooks = IntegerField(
        "Quantidade de livros",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        render_kw={ "value": 1},
    )
    classification = SelectField(
        "Classificação dos livros",
        validators=[DataRequired()],
        choices=[
            ("Didático", "Didático"),
            ("Informática", "Informática"),
            ("Literatura", "Literatura"),
            ("Logística", "Logísitca"),
        ],
    )
    submit = SubmitField("Inserir no livro")


class AddLoanForm(FlaskForm):
    person = StringField(
        "Nome", validators=[DataRequired()], render_kw={"placeholder": "Nome"}
    )
    title = StringField(
        "Título do livro", validators=[DataRequired()], render_kw={"desabled": "desabled"}
    )

    loan_date = DateField("Data do empréstimo", render_kw={"value", datetime.now()})
    return_date = DateField("Data do empréstimo")
    quantity = IntegerField(
        "Quantidade de livros", validators=[DataRequired(), NumberRange(min=1, max=50)]
    )
    submit = SubmitField("Efetuar empréstimo")


class SearchBookForm(FlaskForm):
    search = StringField(
        None,
        validators=[DataRequired()],
        render_kw={
            "placeholder": "digite o título do livro ou nome do autor",
            "class": "form-control",
        },
        id="searchBook",
    )
    submit = SubmitField(
        render_kw={"value": "", "class": "btn submit-btn"},
    )
