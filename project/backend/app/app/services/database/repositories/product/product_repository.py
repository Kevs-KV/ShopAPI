import typing
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSessionTransaction

from services.database.models.product.product import Product
from services.database.repositories.base import Base
from services.database.schemas.product.product import ProductDTO
from utils.database_utils import filter_payload

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]


class ProductRepository(Base):
    model = Product
    DTO = ProductDTO

    async def add_product(self, *,
                          name: str,
                          unit_price: typing.Union[float, Decimal],
                          product_id: typing.Optional[int] = None,
                          description: typing.Optional[str] = None,
                          created_at: typing.Optional[datetime] = None
                          ) -> Model:
        payload = filter_payload(locals())
        return await self._insert(**payload)

    async def all_product(self) -> typing.List[Model]:
        return await self._select_all()

    async def search_product_by_name(self, value: str) -> typing.List[Model]:
        return await self._filter(self.model.name, value)

    async def delete_product(self, product_id: int) -> Model:
        return await self._delete(self.model.id, product_id)
