from celery import shared_task
from celery.utils.log import get_task_logger

from app.services.worker.celery_app import celery_app

logger = get_task_logger(__name__)



@celery_app.task()
def test_celery_start(*args) -> str:
    try:
        return f"{args}"
    except:
        return 'test'
