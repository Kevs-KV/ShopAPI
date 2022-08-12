from celery.utils.log import get_task_logger

from app.services.worker.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"
