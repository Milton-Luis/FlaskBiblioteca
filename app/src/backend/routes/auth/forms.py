from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.backend.models.users import User


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(message="Email é obrigatório")],
        render_kw={"placeholder": "Digite seu email"},
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Senha é obrigatória")],
        render_kw={"placeholder": "Digite sua senha"},
    )
    submit = SubmitField("Entrar")


class AddLibrarianForm(FlaskForm):
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
