import smtplib
from email.mime.text import MIMEText
from starlette.config import Config
from jinja2 import Environment, FileSystemLoader
from starlette.config import Config

# Load .env
config = Config(".env")
FROM_EMAIL = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("app/templates"))


def send_hello_email(to_email: str):
    template = env.get_template("test.html")
    html_content = template.render(name=to_email)

    # Construct HTML email
    msg = MIMEText(html_content, "html")
    msg["Subject"] = "🌞 Good Morning from FastAPI"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(FROM_EMAIL, MAIL_PASSWORD)
        server.send_message(msg)

    print(f"Email sent to {to_email}")
