from fastapi import FastAPI

from app.api.v1.api import api_router
from app.config.settings import settings
from app.utils.application_builder.installation import ApplicationBuilder, DependencyApplicationBuilder
from app.utils.gunicorn_app import StandaloneApplication
from app.utils.logging import configure_logging, LoggingConfig


def app_factory() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app = ApplicationBuilder(DependencyApplicationBuilder(app, settings)).build_app()
    return app


def run_application() -> None:
    app = app_factory()
    stdlib_logconfig_dict = configure_logging(LoggingConfig())
    options = {
        "bind": "%s:%s" % ("0.0.0.0", 8080),
        "worker_class": "uvicorn.workers.UvicornWorker",
        "reload": True,
        "disable_existing_loggers": False,
        "preload_app": True,
        "logconfig_dict": stdlib_logconfig_dict
    }
    gunicorn_app = StandaloneApplication(app, options)
    gunicorn_app.run()


if __name__ == "__main__":
    run_application()
