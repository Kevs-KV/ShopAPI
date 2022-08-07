from typing import Any

import uvicorn
from fastapi import FastAPI

from app.api.v1.api import api_router
from app.config.settings import settings
from app.utils.application_builder.installation import ApplicationBuilder, DependencyApplicationBuilder


def app_factory() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app = ApplicationBuilder(DependencyApplicationBuilder(app, settings)).build_app()
    return app


def run_application(**kwargs: Any) -> None:
    app = app_factory()
    uvicorn.run(app, **kwargs)


if __name__ == "__main__":
    run_application(host="127.0.0.1", port=8080)
