from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv("./.env")
loader = FileSystemLoader(Path(__file__).parent.parent / "templates")
environment = Environment(loader=loader, autoescape=select_autoescape())


def render_template(filename, **data):
    """Render the template with given variables"""
    return environment.get_template(filename).render(**data)


def message_builder(to, subject, body):
    """Build the email message structure"""
    msg = Mail(
        from_email="contact@pedrohferrari.com", to_emails=[to], subject=subject, html_content=body
    )
    return msg


def mail_sender(to, subject, body):
    """Sendgrid email sender"""
    api_key = getenv("SENDGRID_KEY")
    message = message_builder(to, subject, body)
    sendgrid_instance = SendGridAPIClient(api_key)
    sendgrid_instance.send(message)


def register_mail_sender(email, username):
    """Set default register email"""
    return mail_sender(
        to=email,
        subject="Welcome to the Marketplace API",
        body=render_template("emails/register.html", username=username),
    )
