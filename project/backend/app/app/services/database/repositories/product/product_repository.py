import typing
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSessionTransaction

from app.services.database.models.product.product import Product
from app.services.database.repositories.base import Base
from app.services.database.schemas.product.product import ProductDTO, ProductUpdate
from app.utils.database_utils import filter_payload

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]


class ProductRepository(Base):
    model = Product
    DTO = ProductDTO

    async def add_product(self, *,
                          name: str,
                          category_id: int,
                          brand_id: int,
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

    async def get_product(self, product_id: int) -> Model:
        return await self._select_one(self.model.id == product_id)

    async def detail_product(self, product_id: int) -> Model:
        return await self._detail(self.model.id, product_id, self.model.comments)

    async def update_product(self, product_id: int, product: ProductUpdate):
        payload = product.__dict__
        return await self._update(self.model.id == product_id, **payload)

    async def get_list_product(self, page, limit):
        return await self._pagination(page, limit)