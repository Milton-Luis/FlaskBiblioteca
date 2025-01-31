from app.backend.model.models import User
from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, SelectField, StringField,
                     SubmitField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LibrarianForm(FlaskForm):
    firstname = StringField(
        "Nome",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite seu nome"},
    )
    lastname = StringField(
        "Sobrenome",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite seu sobrenome"},
    )
    email = EmailField(
        "E-mail",
        validators=[DataRequired(), Length(min=1, max=65), Email()],
        render_kw={"placeholder": "Digite seu email"},
    )
    phone = StringField(
        "Telefone",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite seu telefone"},
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite sua senha"},
    )
    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(),
            EqualTo("password", "As senhas devem conrresponder"),
        ],
        render_kw={"placeholder": "Confirme sua senha"},
    )
    signup = SubmitField("Inserir Registro")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class StudentForm(FlaskForm):
    firstname = StringField(
        "Nome do Aluno",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o nome do aluno"},
    )
    lastname = StringField(
        "sobrenome do Aluno",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o sobrenome do aluno"},
    )
    phone = StringField(
        "Número do telefone",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o número de telefone"},
    )
    email = StringField(
        "email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o email do aluno"},
    )
    classroom = SelectField(
        "Curso",
        validators=[DataRequired()],
        choices=[
            ("Administração", "Administração"),
            ("Informática", "Informática"),
            ("Logística", "Logística"),
            ("Recursos Humanos", "Recursos Humanos"),
        ],
    )
    grade = StringField(
        "Ano escolar",
        validators=[DataRequired()],
        render_kw={"placeholder": "Digite o ano escolar do aluno. "},
    )
    submit = SubmitField("Inserir aluno")
