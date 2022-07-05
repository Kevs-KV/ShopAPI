from sqlalchemy import select

from services.database.models.user import User
from services.database.repositories.base import Base, Model


class UserRepository(Base):
    model = User


    async def get_user(self, name: str) -> Model:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(select(self.model).
                                           order_by(self.model.name).
                                           filter(self.model.name == name))
            return result.scalars().all()
