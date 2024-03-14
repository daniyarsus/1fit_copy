from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.environ.get("SECRET")
ALGORITHM = os.environ.get("ALGORITHM")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")