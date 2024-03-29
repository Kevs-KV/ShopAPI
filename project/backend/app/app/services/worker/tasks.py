import asyncio

from celery.utils.log import get_task_logger

from app.api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from app.services.worker.base import DatabaseTask
from app.services.worker.celery_app import celery_app
from app.utils.mail_utils import send_mail_register, send_mail_password_reset, send_mail_user_login, send_mail_order

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"


@celery_app.task(name="send_email_register")
def task_send_mail_register(mail_config: dict, email: str, token: str):
    asyncio.run(send_mail_register(mail_config, email, token))
    return True


@celery_app.task(name="send_mail_reset_password")
def task_send_mail_reset_password(mail_config: dict, email: str, token: str):
    asyncio.run(send_mail_password_reset(mail_config, email, token))
    return True


@celery_app.task(name='check_user_activate', base=DatabaseTask)
def task_check_user_activate(email: str):
    repository = task_check_user_activate.repositories[UserRepositoryDependencyMarker]()
    user = asyncio.run(repository.get_by_email(email))
    if user.is_active:
        return {'detail': True}
    asyncio.run(repository.delete_user(email))
    return {'detail': 'user delete'}


@celery_app.task(name='send_mail_user_login')
def task_send_mail_user_login(mail_config: dict, email: str):
    asyncio.run(send_mail_user_login(mail_config, email))
    return True


@celery_app.task(name='send_mail_order_list')
def task_send_mail_order_list(mail_config: dict, order: dict, email: str):
    asyncio.run(send_mail_order(mail_config, order, email))
    return True
