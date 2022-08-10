from celery import shared_task
from celery.utils.log import get_task_logger

from app.services.worker.celery_app import celery_app

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@celery_app.task(acks_late=True)
def test_celery() -> str:
    return f"test task return True"
