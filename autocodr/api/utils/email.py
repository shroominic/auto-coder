from os import getenv

from autocodr.database import models
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient  # type: ignore
from sendgrid.helpers.mail import Mail  # type: ignore

load_dotenv()
email_client = SendGridAPIClient(getenv("SENDGRID_API_KEY"))


# TODO: put this into jinja2 template
async def send_login_email(user: models.User, temp_token: str):
    email_client.send(
        Mail(
            subject="Your Personal Login Link",
            from_email="auth@shroominic.com",
            to_emails=[user.email],
            html_content="Click the following link to log in:<br><br>"
            f" - http://127.0.0.1:8000/login?token={temp_token} - <br><br>"
            "Thanks for using AutoCodr!",
        )
    )
