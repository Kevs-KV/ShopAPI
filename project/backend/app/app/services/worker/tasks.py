import asyncio

from celery.utils.log import get_task_logger

from app.services.worker.celery_app import celery_app
from app.utils.mail_utils import send_mail_register

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"


@celery_app.task(name="send_email_register")
def task_send_mail_register(mail_config: dict, email: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_mail_register(mail_config, email))
    loop.stop()
    return True
