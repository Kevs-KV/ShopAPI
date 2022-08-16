from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config.settings import settings


async def send_mail_register(mail_config: dict, email: str):
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email_register.html") as f:
        template_str = f.read()
    send_mail = FastMail(ConnectionConfig(**mail_config))
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email, ],
        body=template_str,
        subtype="html"
    )
    await send_mail.send_message(message)
    return {'detail': True}