from pathlib import Path

from celery.utils.log import get_task_logger
from fastapi_mail import FastMail, MessageSchema

from app.config.settings import settings
from app.services.worker.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"


@celery_app.task(name="send_email")
def send_mail_register(mail_service: FastMail, email: str):
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email_register") as f:
        template_str = f.read()
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,
        body=template_str,
        subtype="html"
    )
    mail_service.send_message(message)
    return True
