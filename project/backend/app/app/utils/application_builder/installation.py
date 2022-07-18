from typing import no_type_check

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from passlib.context import CryptContext
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.v1.dependencies.database_marker import UserRepositoryDependencyMarker, ProductRepositoryDependencyMarker, \
    CategoryRepositoryDependencyMarker
from api.v1.dependencies.security import JWTAuthenticationMarker, JWTSecurityMarker
from config.settings import settings
from middlewares.process_time_middleware import add_process_time_header
from services.database.repositories.product.category_repository import CategoryRepository
from services.database.repositories.product.product_repository import ProductRepository
from services.database.repositories.user.user_repository import UserRepository
from services.database.session import DatabaseComponents
from services.security.jwt import JWTAuthenticationService, JWTSecurityService
from utils.password_hashing import PasswordHasher


class DependencyApplicationBuilder:

    def __init__(self, app: FastAPI, config: settings):
        self.app = app
        self._settings = config

    def configure_openapi_schema(self) -> None:
        self._openapi_schema = get_openapi(
            title="Kevs",
            version="0.0.1",
            description="This is a very custom OpenAPI schema",
            routes=self.app.routes,
        )
        self._openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        self.app.openapi_schema = self._openapi_schema

    @no_type_check
    def setup_middlewares(self):
        self.app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
        self.app.add_middleware(
            middleware_class=SessionMiddleware,
            secret_key="!secret"
        )

    def configure_application_state(self) -> None:
        db_components = DatabaseComponents(self._settings.SQLALCHEMY_DATABASE_URI)
        password_hasher = PasswordHasher(pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto"))
        self.app.state.db_components = db_components
        self.app.state.config = self._settings
        self.app.dependency_overrides.update({
            UserRepositoryDependencyMarker: lambda: UserRepository(db_components.sessionmaker, password_hasher),
            ProductRepositoryDependencyMarker: lambda: ProductRepository(db_components.sessionmaker),
            CategoryRepositoryDependencyMarker: lambda: CategoryRepository(db_components.sessionmaker),
            JWTAuthenticationMarker: lambda: JWTAuthenticationService(
                user_crud=UserRepository(db_components.sessionmaker, password_hasher),
                password_hasher=password_hasher,
                secret_key=self._settings.SECRET_KEY,
                algorithm="HS256",
                token_expires_in_minutes=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            JWTSecurityMarker: lambda: JWTSecurityService(password_hasher=password_hasher,
                                                          user_crud=UserRepository(db_components.sessionmaker,
                                                                                   password_hasher),
                                                          algorithm="HS256",
                                                          secret_key=self._settings.SECRET_KEY)}

        )


class ApplicationBuilder:

    def __init__(self, builder: DependencyApplicationBuilder):
        self._build = builder

    @property
    def builder(self) -> DependencyApplicationBuilder:
        return self._build

    @builder.setter
    def builder(self, new_builder) -> None:
        self._build = new_builder

    def build_app(self) -> FastAPI:
        self._build.configure_openapi_schema()
        self._build.setup_middlewares()
        self._build.configure_application_state()
        return self._build.app
