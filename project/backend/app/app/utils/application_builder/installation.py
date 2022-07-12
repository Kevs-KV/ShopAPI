from fastapi import FastAPI
from passlib.context import CryptContext

from api.v1.dependencies.database_marker import UserRepositoryDependencyMarker, ProductRepositoryDependencyMarker
from config.settings import settings
from services.database.repositories.product_repository import ProductRepository
from services.database.repositories.user_repository import UserRepository
from services.database.session import DatabaseComponents
from utils.password_hashing import PasswordHasher


class DependencyApplicationBuilder:

    def __init__(self, app: FastAPI, config: settings):
        self.app = app
        self._settings = config

    def configure_application_state(self) -> None:
        db_components = DatabaseComponents(self._settings.SQLALCHEMY_DATABASE_URI)
        password_hasher = PasswordHasher(pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto"))
        self.app.state.db_components = db_components
        self.app.state.config = self._settings
        self.app.dependency_overrides.update({
            UserRepositoryDependencyMarker: lambda: UserRepository(db_components.sessionmaker, password_hasher),
            ProductRepositoryDependencyMarker: lambda: ProductRepository(db_components.sessionmaker),
        })


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
        self._build.configure_application_state()
        return self._build.app
