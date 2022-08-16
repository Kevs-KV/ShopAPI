from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config.settings import settings


async def send_mail_register(mail_config: dict, email: str, token: str):
    mail_config['TEMPLATE_FOLDER'] = Path(settings.EMAIL_TEMPLATES_DIR)
    send_mail = FastMail(ConnectionConfig(**mail_config))
    message = MessageSchema(
        subject="Fastapi-Mail Register module",
        recipients=[email, ],
        template_body={'url': 'http://127.0.0.1:8080/users/register/', 'token': token},
        subtype="html"
    )
    await send_mail.send_message(message, template_name="email_register.html")
    return {'detail': True}
