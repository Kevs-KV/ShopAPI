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


    async def get_order(self, order_id):
        return await self._detail(self.model.id, order_id, self.model.items)
