import asyncio
from typing import Any

import uvicorn
from fastapi import FastAPI

from api.v1.api import api_router
from config.settings import settings
from services.database.models.base import Base
from services.database.session import engine


def app_factory() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app.state.config = settings
    return app


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


def run_application(**kwargs: Any) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_models())
    app = app_factory()
    uvicorn.run(app, **kwargs)


if __name__ == "__main__":
    run_application(host="127.0.0.1", port=8080)
