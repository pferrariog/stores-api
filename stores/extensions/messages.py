from os import getenv

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv("./.env")


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
        body=f"<p>Hello {username} and Congratulations! You successfully signed up!<p/> \
        <p>Get to the /login endpoint to retrieve your access token and start using the API.<p/> \
        <p>Try follow the documentation on the /docs endpoint and enjoy it!",
    )
