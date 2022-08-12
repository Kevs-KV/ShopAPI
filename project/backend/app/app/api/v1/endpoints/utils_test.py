from typing import Any

from fastapi import APIRouter

from app.services.worker.tasks import test_celery_start

api_router = APIRouter()


@api_router.post("/test-celery/", status_code=201)
def test_celery(
        value: int
) -> Any:
    test_celery_start.delay(value)
    return {"msg": f"{value}"}
