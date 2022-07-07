from fastapi import FastAPI

from api.v1.dependencies.database_marker import UserRepositoryDependencyMarker, ProductRepositoryDependencyMarker
from config.settings import settings
from services.database.repositories.product_repository import ProductRepository
from services.database.repositories.user_repository import UserRepository
from services.database.session import DatabaseComponents


class DependencyApplicationBuilder:

    def __init__(self, app: FastAPI, config: settings):
        self.app = app
        self._settings = config

    def configure_application_state(self) -> None:
        db_components = DatabaseComponents(self._settings.SQLALCHEMY_DATABASE_URI)
        self.app.state.db_components = db_components
        self.app.state.config = self._settings
        self.app.dependency_overrides[UserRepositoryDependencyMarker] = lambda: UserRepository(db_components.sessionmaker)
        self.app.dependency_overrides[ProductRepositoryDependencyMarker] = lambda: ProductRepository(db_components.sessionmaker)
        #     UserRepositoryDependencyMarker: lambda: UserRepository(db_components.sessionmaker),
        #     ProductRepositoryDependencyMarker: lambda: ProductRepository(db_components.sessionmaker),
        # })


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
