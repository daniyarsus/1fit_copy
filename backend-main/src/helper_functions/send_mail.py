from smtplib import SMTP_SSL

from settings.mail_config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER
from email.mime.text import MIMEText
from src.helper_functions.random_password import create_random_password


def send_code_to_email_utils(send_to, random_password):
    try:
        text = f"Ваш пароль {random_password}"
        msg = MIMEText(text, "html")
        msg['Subject'] = 'Ваш пароль'
        msg['From'] = f'MAIL_FROM <{MAIL_USERNAME}>'
        msg['To'] = send_to

        # Connect to the email server
        server = SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(e)
        return False


