from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from services.database.models.base import Base


class DatabaseComponents:

    def __init__(self, connection_uri: str, **engine_kwargs) -> None:
        self.__engine_kwargs = engine_kwargs or {}
        self.engine = create_async_engine(url=connection_uri, **self.__engine_kwargs)
        self.sessionmaker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False, autoflush=False

        )

    async def init_models(self):
        session = self.engine
        async with session.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await session.dispose()

    async def get_session(self) -> AsyncSession:
        async with self.sessionmaker as session:
            yield session
