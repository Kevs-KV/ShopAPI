import typing
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from services.database.models.product import ColorEnum, Product
from services.database.session import get_session

Model = typing.TypeVar("Model")

class ProductRepository:
    model = Product

    async def _session(self):
        return await get_session().begin()


    async def add_product(self,
                          name: str,
                          unit_price: typing.Union[float, Decimal],
                          color: ColorEnum,
                          product_id: typing.Optional[int] = None,
                          description: typing.Optional[str] = None,
                          created_at: typing.Optional[datetime] = None
                          ) -> Model:
        print(locals())
        product = Product(locals())
        self._session.add(product)
        await self._session.commit()
        await self._session.refresh(product)
        return product.from_orm(product)