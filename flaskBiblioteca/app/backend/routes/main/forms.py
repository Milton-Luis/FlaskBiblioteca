from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    IntegerField,
    SearchField,
    SelectField,
    StringField,
    SubmitField,
    RadioField,
)
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[DataRequired()],
        render_kw={"placeholder": "Título do livro"},
    )
    author = StringField(
        "Autor",
        validators=[DataRequired()],
        render_kw={"placeholder": "Autor do livro"},
    )
    isbn = StringField(
        "ISBN",
        render_kw={"placeholder": "ISBN do livro"},
    )
    quantity = IntegerField(
        "Quantidade de livros",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        render_kw={"value": 1},
    )
    # classification = SelectField(
    #     "Classificação dos livros",
    #     validators=[DataRequired()],
    #     choices=[
    #         ("Didático", "Didático"),
    #         ("Informática", "Informática"),
    #         ("Literatura", "Literatura"),
    #         ("Logística", "Logísitca"),
    #     ],
    # )
    submit = SubmitField("Adicionar novo livro")


class LendingBooksForm(FlaskForm):

    title = StringField(
        "Título do livro",
        validators=[DataRequired()],
        render_kw={"disabled": "disabled"},
    )
    quantity = IntegerField(
        "Quantidade a ser alugada",
        validators=[DataRequired(), NumberRange(min=1, max=50)], default=1,
    )

    lending_date = DateField(
        "Data do empréstimo",
        render_kw={"disabled": "disabled"},
    )
    return_date = DateField(
        "Data de devolução",
        validators=[DataRequired()],
    )
    submit = SubmitField("Efetuar empréstimo")


class SearchBookForm(FlaskForm):
    search = StringField()
    submit = SubmitField(label="Buscar")



    # later = RadioField()
