from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from starlette.config import Config

# Load .env
config = Config(".env")

# Convert string "True"/"False" to actual booleans
def str_to_bool(value: str) -> bool:
    return value.lower() == "true"

email_send = ConnectionConfig(
    MAIL_USERNAME=config('MAIL_USERNAME'),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM=config("MAIL_FROM"),
    MAIL_PORT=int(config("MAIL_PORT")),
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_STARTTLS=str_to_bool(config("MAIL_TLS")),
    MAIL_SSL_TLS=str_to_bool(config("MAIL_SSL")),
    USE_CREDENTIALS=str_to_bool(config("USE_CREDENTIALS")),
    TEMPLATE_FOLDER='app/email'
)

async def send_email(subject: str, recipient: List[str], context: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=context,
        subtype="html"
    )
    fm = FastMail(email_send)
    await fm.send_message(message)
