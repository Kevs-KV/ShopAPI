import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]
ASTERISK = "*"


class Base:
    model: typing.ClassVar[typing.Type[Model]]

    def __init__(self, session):
        self.__session = session

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
