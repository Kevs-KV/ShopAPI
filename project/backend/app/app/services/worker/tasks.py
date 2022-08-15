import asyncio
from pathlib import Path

from celery.utils.log import get_task_logger
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config.settings import settings
from app.services.worker.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"


@celery_app.task(name="send_email")
def send_mail_register(mail_config: dict, email: str):
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email_register.html") as f:
        template_str = f.read()
    send_mail = FastMail(ConnectionConfig(**mail_config))
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email, ],
        body=template_str,
        subtype="html"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_mail.send_message(message))
    loop.stop()
    return True
