from app.services.database.models.order.order import Item
from app.services.database.repositories.base import Base
from app.services.database.repositories.product.product_repository import Model
from app.utils.database_utils import filter_payload


class ItemRepository(Base):
    model = Item

    async def add_order(self,
                        order_id: int,
                        name: str,
                        product_id: int,
                        quantity: int,
                        price: int
                        ) -> Model:
        payload = filter_payload(locals())
        return await self._insert(**payload)
