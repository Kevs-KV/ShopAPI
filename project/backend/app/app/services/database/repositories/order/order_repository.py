from services.database.models.order.order import Order
from services.database.repositories.base import Base, Model
from services.database.schemas.order.order import OrderDTO


class OrderRepository(Base):
    model = Order

    async def add_order(self,
                        obj_in: OrderDTO,
                        ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)
