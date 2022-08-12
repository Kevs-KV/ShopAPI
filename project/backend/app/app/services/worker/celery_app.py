from celery import Celery

celery_app = Celery("worker", broker="amqp://rabbitmq:5672", include=["app.services.worker.tasks"])


class Config:
    enable_utc = True
    timezone = 'Europe/Minsk'
    broker_url = "amqp://rabbitmq:5672"
    result_backend = "rpc://"


celery_app.config_from_object(Config)
celery_app.autodiscover_tasks()
