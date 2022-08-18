from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config.settings import settings


async def _send_mail_config(template_config: dict) -> FastMail:
    template_config['TEMPLATE_FOLDER'] = Path(settings.EMAIL_TEMPLATES_DIR)
    send_mail = FastMail(ConnectionConfig(**template_config))

    return send_mail


async def _message_config(subject: str, prefix: str, email: str, template_body: dict) -> MessageSchema:
    template_body['url'] = f'http://127.0.0.1:8080/users/{prefix}/'
    message = MessageSchema(
        subject=subject,
        recipients=[email, ],
        template_body=template_body,
        subtype="html"
    )
    return message


async def send_mail_register(template_config: dict, email: str, token: str):
    template_body = {'token': token}
    send_mail = await _send_mail_config(template_config)
    message = await _message_config(subject='register', prefix='register', email=email, template_body=template_body)
    await send_mail.send_message(message, template_name="email_register.html")
    return {'detail': True}


async def send_mail_password_reset(template_config: dict, email: str, token: str):
    template_body = {'token': token}
    send_mail = await _send_mail_config(template_config)
    message = await _message_config(subject='password reset', prefix='password/reset', email=email, template_body=template_body)
    await send_mail.send_message(message, template_name="email_password_reset.html")
    return {'detail': True}
