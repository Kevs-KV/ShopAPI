from typing import Any

from fastapi import APIRouter

from app.services.worker.celery_app import celery_app
from app.services.worker.celery_test import test_celery_start

api_router = APIRouter()


@api_router.post("/test-celery/",  status_code=201)
def test_celery(
    value: int
) -> Any:
    print(celery_app)
    celery_app.send_task("app.services.worker.celery_test.test_celery_start", args=[value])
    return {"msg": f"{value}"}
