from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "app.services.worker.celery_test.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}

celery_app = Celery("worker", broker="amqp://rabbitmq:5672")
celery_app.conf.update(BROKER_URL="amqp://rabbitmq:5672")
celery_app.config_from_object(CELERY_BEAT_SCHEDULE, namespace="CELERY")
celery_app.autodiscover_tasks()