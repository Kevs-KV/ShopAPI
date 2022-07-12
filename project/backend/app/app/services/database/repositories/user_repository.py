from typing import Optional

from pydantic import typing
from sqlalchemy import select

from services.database.models.user import User
from services.database.repositories.base import Base, Model
from services.database.schemas.user import UserCreate
from services.security.jwt import verify_password, get_password_hash
from utils.database_utils import filter_payload


class UserRepository(Base):
    model = User

    def __init__(self, session, password_hasher):
        super().__init__(session)
        self._password_hasher = password_hasher

    async def get_user(self, name: str) -> Model:
        return await self._select_one(self.model.name == name)

    async def get_user_id(self, id: int) -> Model:
        return await self._select_one(self.model.id == id)

    async def get_by_email(self, email: str) -> Model:
        return await self._select_one(self.model.email == email)

    async def create_user(self, obj_in: UserCreate) -> Model:
        payload = obj_in.__dict__
        payload['hashed_password'] = self._password_hasher.get_password_hash(obj_in.password)
        del payload['password']
        return await self._insert(**payload)

    async def delete_user(self, email: str):
        return await self._delete(self.model.email, email)

    async def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not self._password_hasher.verify_password(password, user.hashed_password):
            return None
        return user
