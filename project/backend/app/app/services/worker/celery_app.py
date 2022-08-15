from celery import Celery


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Minsk'
    broker_url = "amqp://rabbitmq:5672"
    result_backend = "rpc://"


def celery_application() -> Celery:
    celery_app = Celery("worker", broker="amqp://rabbitmq:5672", include=["app.services.worker.tasks"])
    celery_app.config_from_object(CeleryConfig)
    return celery_app


celery_app = celery_application()
