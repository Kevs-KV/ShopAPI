from sqlalchemy import select

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

    async def get_detail_order(self, order_id):
        return await self._detail(self.model.id, order_id, self.model.items)

    async def get_by_email(self, email: str) -> Model:
        return await self._select_all(self.model.email == email)

    async def get_list_order(self, page, limit):
        session = await self.get_session()
        async with self._transaction:
            result = await session.execute(
                select(self.model).offset((page - 1) * limit).limit(limit))
        return result.scalars().all()
