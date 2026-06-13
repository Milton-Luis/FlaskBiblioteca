from flask_wtf import FlaskForm
from wtforms.fields import DateField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Email


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
    total_of_books = IntegerField(
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


class BookLoanForm(FlaskForm):
    title = StringField(
        "Título do livro",
        validators=[DataRequired()],
        render_kw={"disabled": "disabled"},
    )

    loan_date = DateField(
        "Data do empréstimo",
        render_kw={"disabled": "disabled"},
    )
    due_date = DateField(
        "Data de devolução",
        validators=[DataRequired()],
    )
    submit = SubmitField("Efetuar empréstimo")


class ReaderForm(FlaskForm):
    firstname = StringField(
        "Nome",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o nome do leitor"},
    )
    lastname = StringField(
        "Sobrenome",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o sobrenome do leitor"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Digite o email do leitor"},
    )
    phone = StringField(
        "Telefone",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o telefone do leitor"},
    )
    submit = SubmitField(label="Adicionar novo leitor")


class SearchBookForm(FlaskForm):
    search = StringField(
        render_kw={
            "placeholder": "Digite o título do livro ou o nome do autor",
            "autocomplete": "off",
        }
    )
    submit = SubmitField(label="Buscar")

    # later = RadioField()
