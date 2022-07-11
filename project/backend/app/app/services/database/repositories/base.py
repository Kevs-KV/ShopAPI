import typing
from contextlib import asynccontextmanager

from sqlalchemy import delete, insert, lambda_stmt, select, exists, func, update
from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession
from sqlalchemy.sql import Executable

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]
ASTERISK = "*"


class Base:
    model: typing.ClassVar[typing.Type[Model]]

    def __init__(self, session):
        self._session = session

    @asynccontextmanager
    async def __transaction(self) -> typing.AsyncGenerator:
        async with self._session.begin() as transaction:
            yield transaction

    @property
    def _transaction(self):
        return self.__transaction()

    async def get_session(self) -> AsyncSession:
        return self._session()

    async def _insert(self, **values: typing.Any) -> Model:
        session = await self.get_session()
        async with self._transaction:
            insert_stmt = (
                insert(self.model)
                    .values(**values)
                    .returning(self.model)
            )
            result = (await session.execute(insert_stmt)).mappings().first()
            await session.commit()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _select_all(self, *clauses: typing.Any) -> typing.List[Model]:
        session = await self.get_session()
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self._transaction:
            result = (
                (await session.execute(typing.cast(Executable, stmt)))
                    .scalars()
                    .all()
            )

        return result

    async def _select_one(self, *clauses: typing.Any) -> Model:
        session = await self.get_session()
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self._transaction:
            result = (
                (await session.execute(typing.cast(Executable, stmt)))
                    .scalars()
                    .first()
            )
        return typing.cast(Model, result)

    async def _update(self, *clauses: typing.Any, **values: typing.Any) -> None:
        session = await self.get_session()
        async with self._transaction:
            stmt = update(self.model).where(*clauses).values(**values).returning(None)
            await session.execute(stmt)
            await session.commit()
        return None

    async def _exists(self, *clauses: typing.Any) -> typing.Optional[bool]:
        session = await self.get_session()
        async with self._transaction:
            stmt = exists(select(self.model).where(*clauses)).select()
            result = (await session.execute(stmt)).scalar()
        return typing.cast(typing.Optional[bool], result)

    async def _delete(self, order: typing.Any, value: typing.Any) -> Model:
        session = await self.get_session()
        async with self._transaction:
            stmt = delete(self.model).where(order == value).returning(ASTERISK)
            result = (await session.execute(stmt)).mappings().first()
            await session.commit()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _filter(self, order: typing.Any, value: typing.Any) -> Model:
        session = await self.get_session()
        async with self._transaction:
            result = await session.execute(
                select(self.model).order_by(order).filter(order == value))
        return result.scalars().all()

    async def _count(self) -> int:
        session = await self.get_session()
        async with self._transaction:
            count = (await session.execute(func.count(ASTERISK))).scalars().first()
        return typing.cast(int, count)

    def _convert_to_model(self, kwargs) -> Model:
        return self.model(**kwargs)
