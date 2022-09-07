from typing import AsyncGenerator, Any

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings
from app.utils.application_builder.installation import ApplicationBuilder, DependencyApplicationBuilder


@pytest.fixture(scope="module")
def setting() -> Settings:
    return Settings()


@pytest.fixture(scope="module")
def app(apply_migrations: None) -> FastAPI:
    settings = Settings()
    director = ApplicationBuilder(DependencyApplicationBuilder(app, settings)).build_app()
    return director.build_app()


@pytest.fixture(scope="module")
async def initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI, Any]:
    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="module")
def session_maker(initialized_app: FastAPI) -> sessionmaker:
    return initialized_app.state.db_components.sessionmaker


@pytest.fixture(scope="module")
async def client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
            app=initialized_app,
            base_url="http://test",
            headers={"Content-Type": "application/json"},
    ) as client:  # type: AsyncClient
        yield client
