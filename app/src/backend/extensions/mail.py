from threading import Thread

from flask import current_app, render_template
from flask_mailman import EmailMessage, Mail

mail = Mail()


def send_async_email(app, msg: EmailMessage):
    """
    The function is designed to send an email asynchronously using the Flask-Mail extension in a Flask web application."""

    with app.app_context():
        msg.send()


def send_email(to, subject, template, **kwargs):
    """sender email function

    Args:
        * to ([str]): [receiver.]
        * subject ([str]): [subject.]
        * template ([file]): [html template that contains some information, depending on the function that uses it.For example, an email confirmation template]

    Returns:
        [thread_email]: [send asynchronous e-mail.]
    """

    app = current_app._get_current_object()
    
    message = EmailMessage(
        subject=f"{app.config['MAIL_SUBJECT_PREFIX']} - {subject}",
        body = render_template(f"{template}.html", **kwargs),
        from_email=app.config["MAIL_DEFAULT_SENDER"],
        to=[to],
    )

    message.content_subtype = "html"
    thread_email = Thread(target=send_async_email, args=[app, message]).start()
    return thread_email


def init_app(app):
    return mail.init_app(app)
