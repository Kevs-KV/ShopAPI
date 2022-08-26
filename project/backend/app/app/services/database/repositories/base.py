import typing
from abc import ABCMeta
from contextlib import asynccontextmanager

from sqlalchemy import delete, insert, lambda_stmt, select, exists, func, update
from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker
from sqlalchemy.sql import Executable

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]
ASTERISK = "*"


class Base(metaclass=ABCMeta):
    model: typing.ClassVar[typing.Type[Model]]

    def __init__(self, session: typing.Union[sessionmaker, AsyncSession]) -> None:
        if isinstance(session, sessionmaker):
            self._session: AsyncSession = typing.cast(AsyncSession, session())
        else:
            self._session = session

    @asynccontextmanager
    async def __transaction(self) -> typing.AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield   # type: ignore

    @property
    def _transaction(self) -> TransactionContext:
        return self.__transaction()


    async def _insert(self, **values: typing.Any) -> Model:
        async with self._transaction:
            insert_stmt = (
                insert(self.model)
                    .values(**values)
                    .returning(self.model)
            )
            result = (await self._session.execute(insert_stmt)).mappings().first()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _select_all(self, *clauses: typing.Any) -> typing.List[Model]:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self._transaction:
            result = (
                (await self._session.execute(typing.cast(Executable, stmt)))
                    .scalars()
                    .all()
            )

        return result

    async def _select_one(self, *clauses: typing.Any) -> Model:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self._transaction:
            result = (
                (await self._session.execute(typing.cast(Executable, stmt)))
                    .scalars()
                    .first()
            )
        return typing.cast(Model, result)

    async def _update(self, *clauses: typing.Any, **values: typing.Any) -> None:
        async with self._transaction:
            stmt = update(self.model).where(*clauses).values(**values).returning(None)
            await self._session.execute(stmt)
            await self._session.commit()
        return None

    async def _exists(self, *clauses: typing.Any) -> typing.Optional[bool]:
        async with self._transaction:
            stmt = exists(select(self.model).where(*clauses)).select()
            result = (await self._session.execute(stmt)).scalar()
        return typing.cast(typing.Optional[bool], result)

    async def _delete(self, order: typing.Any, value: typing.Any) -> Model:
        async with self._transaction:
            stmt = delete(self.model).where(order == value).returning(ASTERISK)
            result = (await self._session.execute(stmt)).mappings().first()
            await self._session.commit()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _filter(self, order: typing.Any, value: typing.Any) -> Model:
        async with self._transaction:
            result = await self._session.execute(
                select(self.model).order_by(order).filter(order == value))
        return result.scalars().all()

    async def _detail(self, order: typing.Any, value: typing.Any, inload: typing.Any) -> Model:
        async with self._transaction:
            result = await self._session.execute(
                select(self.model).order_by(order).filter(order == value).options(
                    selectinload(inload)))
        return typing.cast(Model, result.scalars().first())

    async def _count(self) -> int:
        async with self._transaction:
            count = (await self._session.execute(func.count(ASTERISK))).scalars().first()
        return typing.cast(int, count)

    async def _pagination(self, page, limit) -> typing.List[Model]:
        async with self._transaction:
            result = await self._session.execute(
                select(self.model).offset((page - 1) * limit).limit(limit))
        return result.scalars().all()

    def _convert_to_model(self, kwargs) -> Model:
        return self.model(**kwargs)
