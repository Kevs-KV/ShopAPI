import typing
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSessionTransaction

from services.database.models.product import Product
from services.database.repositories.base import Base
from services.database.schemas.product import ProductDTO

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]


class ProductRepository(Base):
    model = Product
    DTO = ProductDTO

    async def add_product(self,
                          name: str,
                          unit_price: typing.Union[float, Decimal],
                          description: typing.Optional[str] = None,
                          created_at: typing.Optional[datetime] = None,
                          ) -> Model:
        product = Product(name=name, unit_price=unit_price, description=description, created_at=created_at)
        async with self._transaction:
            session = self.get_session()
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    async def all_product(self) -> typing.List[Model]:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def search_product(self, value: str) -> typing.List[Model]:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(
                select(self.model).order_by(self.model.name).filter(self.model.name == value))
            return result.scalars().all()
