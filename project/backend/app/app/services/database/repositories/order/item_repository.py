from services.database.models.order.order import Item
from services.database.repositories.base import Base
from services.database.repositories.product.product_repository import Model
from utils.database_utils import filter_payload


class ItemRepository(Base):
    model = Item

    async def add_order(self,
                        order_id: int,
                        product_id: int,
                        quantity: int,
                        price: int
                        ) -> Model:
        payload = filter_payload(locals())
        return await self._insert(**payload)
