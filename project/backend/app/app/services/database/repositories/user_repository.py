from typing import Optional

from pydantic import typing
from sqlalchemy import select

from services.database.models.user import User
from services.database.repositories.base import Base, Model
from services.database.schemas.user import UserCreate
from services.security.jwt import verify_password, get_password_hash


class UserRepository(Base):
    model = User

    async def get_user(self, name: str) -> Model:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(select(self.model).
                                           order_by(self.model.name).
                                           filter(self.model.name == name))
            return typing.cast(Model, result.scalars().first())

    async def get_user_id(self, id: int) -> Model:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(select(self.model).
                                           order_by(self.model.id).
                                           filter(self.model.id == id))

            return typing.cast(Model, result.scalars().first())

    async def get_by_email(self, email: str) -> Model:
        async with self._transaction:
            session = self.get_session()
            result = await session.execute(select(self.model).
                                           order_by(self.model.email).
                                           filter(self.model.email == email))
            return typing.cast(Model, result.scalars().first())

    async def create_user(self, obj_in: UserCreate) -> User:
        user = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        async with self._transaction:
            session = self.get_session()
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email=email)
        user = user
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
