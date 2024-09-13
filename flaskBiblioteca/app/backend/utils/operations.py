from app.backend.extensions.database import db
from app.backend.extensions.mail import send_email
from app.backend.extensions.security import generate_confirmation_token
from app.backend.model.models import Admin, User
from flask import current_app, flash
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError


def check_attribute(model: type, column_name: str) -> None:
    if not hasattr(model, column_name):
        raise ValueError(f"Invalid column name: {column_name}")


class Services:
    @staticmethod
    def new_register(model: type, **kwargs):
        check_attribute(model, **kwargs)
        try:
            if Admin.check_admin_permission(model):
                content = model(**kwargs)
                db.session.add(content)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def access_confirmation(user: User):
        if current_app.config["ROLE_PREFIX"] in user.roles.rolename:
            token = generate_confirmation_token(user.email)
            send_email(
                user.email,
                "Confirme seu email",
                "auth_pages/email/confirm",
                user=user,
                token=token,
            )
            flash("Um email de confirmação foi enviado a você", "info")
        else:
            flash("Erro ao enviar o email de confirmação", "danger")

    @staticmethod
    def get_all_records(model: type, column_name: str) -> list:
        try:
            content = db.session.query(model).order_by(asc(column_name))
            return content
        except Exception as e:
            raise f"Ocorreu um erro ao retornar os valores ordenados - {e}"
        finally:
            db.session.close()
    
    @staticmethod
    def get_one_record(model: type, id: int) -> object:
        try:
            content = db.session.query(model).get(id)
            return content
        except Exception:
            flash("Não foi possível encontrar o registro correspondente.", "danger")
        finally:
            db.session.close()

    @staticmethod
    def get_first_record(model: type, **kwargs) -> object:
        try:
            content = db.session.query(model).filter_by(**kwargs).first_or_404()
            return content
        except Exception as e:
            raise e
        finally:
            db.session.close()

    @staticmethod
    def delete_value(model: type, id: int):
        try:
            if Admin.check_admin_permission(model):
                content = Services.get_one_value(model, id)
                if content:
                    db.session.delete(content)
                    db.session.commit()
                    return True
                else:
                    return False
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()
