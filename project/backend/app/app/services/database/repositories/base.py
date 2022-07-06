import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession
from sqlalchemy.orm import sessionmaker

from services.database.session import engine

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]
ASTERISK = "*"

class Base:
    model: typing.ClassVar[typing.Type[Model]]
    __session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    @contextlib.asynccontextmanager
    async def __transaction(self) -> typing.AsyncGenerator:
        async with self.__session.begin() as transaction:
            yield transaction

    @property
    def _transaction(self):
        return self.__transaction()

    def get_session(self) -> AsyncSession:
        return self.__session()

    def _convert_to_model(self, kwargs) -> Model:
        return self.model(**kwargs)