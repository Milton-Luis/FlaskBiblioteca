from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email é obrigatório"),
            Email(message="Email invalido"),
        ],
        render_kw={"placeholder": "Digite seu email"},
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Senha é obrigatória")],
        render_kw={"placeholder": "Digite sua senha"},
    )
    submit = SubmitField("Entrar")

