from sqlalchemy import select

from app.services.database.models.order.order import Order
from app.services.database.repositories.base import Base, Model
from app.services.database.schemas.order.order import OrderDTO


class OrderRepository(Base):
    model = Order

    async def add_order(self,
                        obj_in: OrderDTO,
                        ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)

    async def get_detail_order(self, order_id):
        return await self._detail(self.model.id, order_id, self.model.items)

    async def get_by_email(self, email: str) -> Model:
        return await self._select_all(self.model.email == email)

    async def get_list_order(self, page, limit):
        return await self._pagination(page, limit)