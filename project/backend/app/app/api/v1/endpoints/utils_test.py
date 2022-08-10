from typing import Any

from fastapi import APIRouter

from app.services.worker.celery_app import celery_app

api_router = APIRouter()


@api_router.post("/test-celery/", status_code=201)
def test_celery() -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.services.worker.test_celery")
    return {"detail": True}
